import XCTest
@testable import Questly
@testable import QuestCore

@MainActor
final class GameModelTests: XCTestCase {
    private enum WriteFault { case none, beforeReplacement, afterReplacement }
    private final class FaultControl { var fault: WriteFault = .none }

    private func withStore(_ body: (SaveStore, FaultControl, URL) throws -> Void) throws {
        let directory = FileManager.default.temporaryDirectory.appendingPathComponent("questly-model-qe-" + UUID().uuidString)
        defer { try? FileManager.default.removeItem(at: directory) }
        let control = FaultControl()
        let store = SaveStore(directory: directory) { data, url in
            if control.fault == .beforeReplacement { throw CocoaError(.fileWriteOutOfSpace) }
            try data.write(to: url, options: .atomic)
            if control.fault == .afterReplacement { throw CocoaError(.fileWriteUnknown) }
        }
        try body(store, control, directory)
    }

    private func checkpoints(_ directory: URL) throws -> [String: Data] {
        let files = try FileManager.default.contentsOfDirectory(at: directory, includingPropertiesForKeys: nil)
        return try Dictionary(uniqueKeysWithValues: files.map { ($0.lastPathComponent, try Data(contentsOf: $0)) })
    }

    func testPostReplacementErrorFreezesEditsUntilReloadWithoutReplayingDelivery() throws {
        try withStore { store, control, directory in
            let model = GameModel(store: store)
            XCTAssertTrue(model.ready)
            model.toggle(0)
            model.toggle(3)
            let before = model.progress
            control.fault = .afterReplacement

            model.launch()
            XCTAssertFalse(model.ready, "A throwing save has an uncertain commit outcome; block stale edits.")
            XCTAssertNotNil(model.storageIssue)
            XCTAssertFalse(model.deliveredNotice)
            XCTAssertEqual(model.progress, before, "Do not announce a delivery before write acknowledgement.")
            let committed = try store.load().progress
            XCTAssertEqual(committed.active.cargo.trips, [[0, 3]])
            let diskAfterFailure = try checkpoints(directory)

            // Even after the I/O issue clears, normal controls must not overwrite the newer checkpoint.
            control.fault = .none
            model.toggle(4)
            model.launch()
            model.undo()
            model.restart()
            model.hint()
            model.changeLanguage()
            model.setMotion(false)
            model.setMode(.engineer)
            model.select(.comet)
            model.navigate(.cargo)
            XCTAssertEqual(model.progress, before)
            XCTAssertEqual(try checkpoints(directory), diskAfterFailure)

            model.reload()
            XCTAssertTrue(model.ready)
            XCTAssertNil(model.storageIssue)
            XCTAssertEqual(model.progress, committed)
            XCTAssertEqual(model.cargo.trips, [[0, 3]], "Reload reconciles the save; it never replays launch.")
            XCTAssertTrue(model.cargo.load.isEmpty)
            model.toggle(4)
            model.launch()
            XCTAssertEqual(model.cargo.trips, [[0, 3], [4]])
            XCTAssertEqual(try store.load().progress, model.progress)
        }
    }

    func testPreReplacementFailureKeepsCheckpointAndRequiresSuccessfulReload() throws {
        try withStore { store, control, directory in
            let model = GameModel(store: store)
            model.toggle(0)
            model.toggle(3)
            let before = model.progress
            let beforeBytes = try checkpoints(directory)
            control.fault = .beforeReplacement

            model.launch()
            XCTAssertFalse(model.ready)
            XCTAssertFalse(model.deliveredNotice)
            XCTAssertEqual(model.progress, before)
            XCTAssertEqual(try store.load().progress, before)
            XCTAssertEqual(try checkpoints(directory), beforeBytes)

            model.reload()
            XCTAssertFalse(model.ready, "Failed recovery must keep game controls unavailable.")
            XCTAssertNotNil(model.storageIssue)
            XCTAssertEqual(try checkpoints(directory), beforeBytes)

            control.fault = .none
            model.reload()
            XCTAssertTrue(model.ready)
            XCTAssertNil(model.storageIssue)
            XCTAssertEqual(model.progress, before)
            model.launch()
            XCTAssertEqual(model.cargo.trips, [[0, 3]])
            XCTAssertEqual(try store.load().progress, model.progress)
        }
    }

    func testReloadClearsDeliveryAndRuleFeedbackWhenReconcilingAnotherProfile() throws {
        try withStore { store, control, _ in
            let model = GameModel(store: store)
            // Both profiles already use the cargo screen, so stale feedback would be visible
            // immediately after recovery instead of being cleared by a navigation action.
            model.select(.comet)
            model.navigate(.cargo)
            model.select(.fern)
            model.navigate(.cargo)
            model.toggle(0)
            model.toggle(3)
            model.launch()
            XCTAssertTrue(model.deliveredNotice)
            XCTAssertEqual(model.cargo.trips, [[0, 3]])

            control.fault = .afterReplacement
            model.select(.comet)
            XCTAssertFalse(model.ready)
            XCTAssertEqual(model.progress.activeAvatar, .fern)
            XCTAssertEqual(try store.load().progress.activeAvatar, .comet)

            control.fault = .none
            model.reload()
            XCTAssertTrue(model.ready)
            XCTAssertEqual(model.progress.activeAvatar, .comet)
            XCTAssertEqual(model.profile.destination, .cargo)
            XCTAssertTrue(model.cargo.trips.isEmpty)
            XCTAssertFalse(model.deliveredNotice, "Comet has not delivered anything; Fern's success notice must not survive reload.")
            XCTAssertNil(model.feedback)

            // Exercise a rejected-move reason as well as the success banner.
            model.toggle(1)
            model.launch()
            XCTAssertEqual(model.feedback, .crane)
            control.fault = .afterReplacement
            model.select(.fern)
            XCTAssertFalse(model.ready)
            XCTAssertEqual(try store.load().progress.activeAvatar, .fern)

            control.fault = .none
            model.reload()
            XCTAssertTrue(model.ready)
            XCTAssertEqual(model.progress.activeAvatar, .fern)
            XCTAssertEqual(model.cargo.trips, [[0, 3]])
            XCTAssertNil(model.feedback, "Comet's rejected-move reason must not describe Fern's recovered plan.")
            XCTAssertFalse(model.deliveredNotice)
            XCTAssertEqual(try store.load().progress, model.progress)
        }
    }
}
