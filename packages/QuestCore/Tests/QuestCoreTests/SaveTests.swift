import XCTest
import CryptoKit
@testable import QuestCore

final class SaveTests: XCTestCase {
    var directory: URL!
    override func setUpWithError() throws {
        directory = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        try FileManager.default.createDirectory(at: directory, withIntermediateDirectories: true)
    }
    override func tearDownWithError() throws { try FileManager.default.removeItem(at: directory) }
    func slot(_ index: Int) -> URL { directory.appendingPathComponent("checkpoint-\(index).json") }

    func testColdRelaunchProfilesModesPreferencesAndSelectedCargo() throws {
        var p = Progress()
        p.active.cargo.toggle(0); p.active.cargo.toggle(3)
        XCTAssertTrue(p.active.cargo.launch(.explorer).ok)
        p.active.mode = .engineer
        p.active.cargo.toggle(2)
        p.active.destination = .cargo
        p.activeAvatar = .comet
        p.active.cargo.toggle(4)
        p.language = .zh; p.motion = false
        try SaveStore(directory: directory).save(p)
        let relaunched = try SaveStore(directory: directory).load()
        XCTAssertEqual(relaunched.progress, p)
        XCTAssertFalse(relaunched.recovered)
        var restored = relaunched.progress
        XCTAssertEqual(restored.active.cargo.load, [4])
        restored.activeAvatar = .fern
        XCTAssertEqual(restored.active.cargo.load, [2])
        XCTAssertEqual(restored.active.destination, .cargo)
        restored.active.mode = .explorer
        XCTAssertEqual(restored.active.cargo.trips, [[0, 3]])
    }

    func testCorruptNewestRecoversPreviousAndCanSaveAgain() throws {
        let store = SaveStore(directory: directory)
        let old = Progress()
        try store.save(old)
        var next = old; next.active.cargo.toggle(0)
        try store.save(next)
        try Data("broken".utf8).write(to: slot(1))
        let restored = try store.load()
        XCTAssertEqual(restored.progress, old)
        XCTAssertTrue(restored.recovered)
        try store.save(next)
        XCTAssertEqual(try store.load().progress, next)
        XCTAssertFalse(try store.load().recovered)
    }

    func testInterruptedWriteRetainsLastCheckpoint() throws {
        var old = Progress(); old.active.cargo.toggle(0)
        try SaveStore(directory: directory).save(old)
        let failing = SaveStore(directory: directory) { _, url in
            try Data("partial write".utf8).write(to: url)
            throw CocoaError(.fileWriteOutOfSpace)
        }
        var next = old; next.active.cargo.toggle(3)
        XCTAssertThrowsError(try failing.save(next))
        XCTAssertEqual(try SaveStore(directory: directory).load().progress, old)
        XCTAssertTrue(try SaveStore(directory: directory).load().recovered)
    }

    func testUncommittedTemporaryFileIgnored() throws {
        let p = Progress()
        try SaveStore(directory: directory).save(p)
        try Data("uncommitted staging content".utf8).write(to: directory.appendingPathComponent(".checkpoint.tmp"))
        XCTAssertEqual(try SaveStore(directory: directory).load().progress, p)
    }

    func testBothDamagedBlockWritesAndPreserveEvidence() throws {
        try Data("broken0".utf8).write(to: slot(0))
        try Data("broken1".utf8).write(to: slot(1))
        let store = SaveStore(directory: directory)
        XCTAssertThrowsError(try store.load()) { XCTAssertEqual($0 as? SaveError, .noRecoverableSave) }
        XCTAssertThrowsError(try store.save(Progress()))
        XCTAssertEqual(try String(contentsOf: slot(0), encoding: .utf8), "broken0")
        XCTAssertEqual(try String(contentsOf: slot(1), encoding: .utf8), "broken1")
    }

    func testFutureSchemaBlocksRollbackEvenWithValidOlderSlot() throws {
        try SaveStore(directory: directory).save(Progress())
        try Data(#"{"version":2}"#.utf8).write(to: slot(1))
        XCTAssertThrowsError(try SaveStore(directory: directory).load()) { XCTAssertEqual($0 as? SaveError, .newerVersion) }
        XCTAssertThrowsError(try SaveStore(directory: directory).save(Progress()))
    }

    func testChecksumTamperingRecoversAndInvalidStateCannotBeSaved() throws {
        let store = SaveStore(directory: directory)
        let p = Progress()
        try store.save(p); try store.save(p)
        var json = try XCTUnwrap(JSONSerialization.jsonObject(with: Data(contentsOf: slot(1))) as? [String: Any])
        json["generation"] = 9000
        try JSONSerialization.data(withJSONObject: json).write(to: slot(1))
        XCTAssertTrue(try store.load().recovered)
        var bad = p; bad.profiles.removeLast()
        XCTAssertThrowsError(try store.save(bad)) { XCTAssertEqual($0 as? SaveError, .invalidState) }
    }

    func testContentRevisionRequiresMigrationRatherThanReset() throws {
        let store = SaveStore(directory: directory)
        try store.save(Progress())
        var envelope = try XCTUnwrap(JSONSerialization.jsonObject(with: Data(contentsOf: slot(0))) as? [String: Any])
        let payload = try XCTUnwrap(Data(base64Encoded: envelope["payload"] as! String))
        var content = try XCTUnwrap(JSONSerialization.jsonObject(with: payload) as? [String: Any])
        content["contentChecksum"] = "old-content"
        let changed = try JSONSerialization.data(withJSONObject: content)
        envelope["payload"] = changed.base64EncodedString()
        envelope["checksum"] = SHA256.hash(data: Data("1:1:".utf8) + changed).map { String(format: "%02x", $0) }.joined()
        try JSONSerialization.data(withJSONObject: envelope).write(to: slot(0))
        XCTAssertThrowsError(try store.load()) { XCTAssertEqual($0 as? SaveError, .changedContent) }
    }

    func testSaveFailureDoesNotDestroyPreviousFile() throws {
        let p = Progress()
        try SaveStore(directory: directory).save(p)
        let bytes = try Data(contentsOf: slot(0))
        let store = SaveStore(directory: directory) { _, _ in throw CocoaError(.fileWriteNoPermission) }
        XCTAssertThrowsError(try store.save(p))
        XCTAssertEqual(try Data(contentsOf: slot(0)), bytes)
    }
}
