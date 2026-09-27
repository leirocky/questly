import XCTest
import CryptoKit
@testable import QuestCore

/// Independent QE fault injection. All directories contain synthetic test progress only.
final class QESaveFaultTests: XCTestCase {
    private var directory: URL!

    override func setUpWithError() throws {
        directory = FileManager.default.temporaryDirectory.appendingPathComponent("questly-qe-" + UUID().uuidString)
        try FileManager.default.createDirectory(at: directory, withIntermediateDirectories: true)
    }

    override func tearDownWithError() throws {
        try FileManager.default.removeItem(at: directory)
    }

    private func slot(_ index: Int) -> URL {
        directory.appendingPathComponent("checkpoint-\(index).json")
    }

    private func editedEnvelope(_ data: Data, generation: UInt64? = nil,
                                edit: (inout [String: Any]) -> Void = { _ in }) throws -> Data {
        var envelope = try XCTUnwrap(JSONSerialization.jsonObject(with: data) as? [String: Any])
        let payload = try XCTUnwrap(Data(base64Encoded: try XCTUnwrap(envelope["payload"] as? String)))
        var contents = try XCTUnwrap(JSONSerialization.jsonObject(with: payload) as? [String: Any])
        edit(&contents)
        let changed = try JSONSerialization.data(withJSONObject: contents, options: .sortedKeys)
        if let generation { envelope["generation"] = NSNumber(value: generation) }
        let value = try XCTUnwrap(envelope["generation"] as? NSNumber).uint64Value
        envelope["payload"] = changed.base64EncodedString()
        envelope["checksum"] = SHA256.hash(data: Data("1:\(value):".utf8) + changed)
            .map { String(format: "%02x", $0) }.joined()
        return try JSONSerialization.data(withJSONObject: envelope, options: .sortedKeys)
    }

    func testEveryTruncationOfNewestCheckpointRecoversOlderBytesWithoutMutatingFiles() throws {
        let store = SaveStore(directory: directory)
        var older = Progress()
        older.active.cargo.toggle(0)
        try store.save(older)
        var newer = older
        newer.active.cargo.toggle(3)
        XCTAssertTrue(newer.active.cargo.launch(.explorer).ok)
        try store.save(newer)
        let priorBytes = try Data(contentsOf: slot(0))
        let fullBytes = try Data(contentsOf: slot(1))
        for length in 0..<fullBytes.count {
            let truncated = fullBytes.prefix(length)
            try truncated.write(to: slot(1))
            let restored = try SaveStore(directory: directory).load()
            XCTAssertEqual(restored.progress, older, "Truncation length \(length)")
            XCTAssertTrue(restored.recovered, "Truncation length \(length)")
            XCTAssertEqual(try Data(contentsOf: slot(0)), priorBytes)
            XCTAssertEqual(try Data(contentsOf: slot(1)), truncated)
        }
        print("QE: tested all \(fullBytes.count) truncated prefixes of the newer checkpoint")
    }

    func testAuthenticatedIllegalCargoHistoryFallsBackRatherThanEnteringRules() throws {
        let store = SaveStore(directory: directory)
        let prior = Progress()
        try store.save(prior)
        try store.save(prior)
        let bytes = try Data(contentsOf: slot(1))
        // Recompute checksum deliberately: integrity must include semantic validity.
        let malformed = try editedEnvelope(bytes) { payload in
            var profiles = payload["profiles"] as! [[String: Any]]
            var cargo = profiles[0]["explorer"] as! [String: Any]
            cargo["trips"] = [[1], [0]] // Beams arrive before the crane.
            profiles[0]["explorer"] = cargo
            payload["profiles"] = profiles
        }
        try malformed.write(to: slot(1))
        let loaded = try store.load()
        XCTAssertTrue(loaded.recovered)
        XCTAssertEqual(loaded.progress, prior)
        XCTAssertEqual(try Data(contentsOf: slot(1)), malformed)
    }

    func testDuplicateProfileIDsAreRejectedEvenWithCorrectChecksum() throws {
        let store = SaveStore(directory: directory)
        try store.save(Progress())
        let malformed = try editedEnvelope(Data(contentsOf: slot(0))) { payload in
            var profiles = payload["profiles"] as! [[String: Any]]
            profiles[1]["id"] = profiles[0]["id"]
            payload["profiles"] = profiles
        }
        try malformed.write(to: slot(0))
        XCTAssertThrowsError(try store.load()) { XCTAssertEqual($0 as? SaveError, .noRecoverableSave) }
        XCTAssertThrowsError(try store.save(Progress()))
        XCTAssertEqual(try Data(contentsOf: slot(0)), malformed)
    }

    func testFuturePayloadSchemaPreservesBothSlotsAndBlocksWrites() throws {
        let store = SaveStore(directory: directory)
        try store.save(Progress())
        try store.save(Progress())
        let prior = try Data(contentsOf: slot(0))
        let future = try editedEnvelope(Data(contentsOf: slot(1))) { $0["version"] = 2 }
        try future.write(to: slot(1))
        XCTAssertThrowsError(try store.load()) { XCTAssertEqual($0 as? SaveError, .newerVersion) }
        XCTAssertThrowsError(try store.save(Progress())) { XCTAssertEqual($0 as? SaveError, .newerVersion) }
        XCTAssertEqual(try Data(contentsOf: slot(0)), prior)
        XCTAssertEqual(try Data(contentsOf: slot(1)), future)
    }

    func testOversizedAndUnreadableSlotsDoNotBecomeFreshEmptyProgress() throws {
        let store = SaveStore(directory: directory)
        var prior = Progress()
        prior.active.cargo.toggle(4)
        try store.save(prior)
        let oversized = Data(repeating: 0x58, count: 1_048_577)
        try oversized.write(to: slot(1))
        let loaded = try store.load()
        XCTAssertEqual(loaded.progress, prior)
        XCTAssertTrue(loaded.recovered)
        XCTAssertEqual(try Data(contentsOf: slot(1)), oversized)
        try FileManager.default.removeItem(at: slot(0))
        XCTAssertThrowsError(try store.load()) { XCTAssertEqual($0 as? SaveError, .noRecoverableSave) }
        try FileManager.default.removeItem(at: slot(1))
        // A directory at a checkpoint path provokes a real read I/O error on macOS.
        try FileManager.default.createDirectory(at: slot(0), withIntermediateDirectories: false)
        XCTAssertThrowsError(try store.load())
        XCTAssertThrowsError(try store.save(Progress()))
        var isDirectory: ObjCBool = false
        XCTAssertTrue(FileManager.default.fileExists(atPath: slot(0).path, isDirectory: &isDirectory))
        XCTAssertTrue(isDirectory.boolValue)
    }

    func testGenerationExhaustionCannotWrapAndOverwriteNewest() throws {
        let store = SaveStore(directory: directory)
        try store.save(Progress())
        let exhausted = try editedEnvelope(Data(contentsOf: slot(0)), generation: .max)
        try exhausted.write(to: slot(0))
        XCTAssertEqual(try store.load().progress, Progress())
        XCTAssertThrowsError(try store.save(Progress())) { XCTAssertEqual($0 as? SaveError, .newerVersion) }
        XCTAssertEqual(try Data(contentsOf: slot(0)), exhausted)
        XCTAssertFalse(FileManager.default.fileExists(atPath: slot(1).path))
    }

    func testPostReplacementIOErrorHasAnUncertainCommitOutcome() throws {
        var prior = Progress()
        prior.active.cargo.toggle(0)
        prior.active.cargo.toggle(3)
        try SaveStore(directory: directory).save(prior)
        let priorBytes = try Data(contentsOf: slot(0))
        var delivered = prior
        XCTAssertTrue(delivered.active.cargo.launch(.explorer).ok)
        let failing = SaveStore(directory: directory) { data, url in
            try data.write(to: url, options: .atomic)
            // Models FileHandle open/synchronize failing after successful atomic replacement.
            throw CocoaError(.fileWriteUnknown)
        }
        XCTAssertThrowsError(try failing.save(delivered))
        XCTAssertEqual(try Data(contentsOf: slot(0)), priorBytes)
        let reopened = try SaveStore(directory: directory).load()
        XCTAssertEqual(reopened.progress, delivered)
        XCTAssertFalse(reopened.recovered)
        XCTAssertNotEqual(reopened.progress, prior)
        print("QE: an error after atomic replacement leaves the newer complete checkpoint visible; callers must reload before further edits")
    }

    func testRollbackRecoveryKeepsOtherProfileAndOtherDifficultyIntact() throws {
        let store = SaveStore(directory: directory)
        var prior = Progress()
        prior.active.cargo.toggle(4)
        prior.active.mode = .engineer
        prior.active.cargo.toggle(0)
        prior.active.cargo.toggle(3)
        XCTAssertTrue(prior.active.cargo.launch(.engineer).ok)
        prior.activeAvatar = .comet
        prior.active.cargo.toggle(5)
        prior.language = .zh
        prior.motion = false
        try store.save(prior)
        var next = prior
        next.active.mode = .engineer
        next.active.cargo.toggle(2)
        try store.save(next)
        try Data("interrupted newest write".utf8).write(to: slot(1))
        let loaded = try SaveStore(directory: directory).load()
        XCTAssertEqual(loaded.progress, prior)
        XCTAssertTrue(loaded.recovered)
        XCTAssertEqual(loaded.progress.profiles.first { $0.id == .fern }?.explorer.load, [4])
        XCTAssertEqual(loaded.progress.profiles.first { $0.id == .fern }?.engineer.trips, [[0, 3]])
        XCTAssertEqual(loaded.progress.profiles.first { $0.id == .comet }?.explorer.load, [5])
        XCTAssertEqual(loaded.progress.profiles.first { $0.id == .comet }?.engineer.load, [])
    }
}
