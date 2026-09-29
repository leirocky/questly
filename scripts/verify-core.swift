// Standalone integration verification. Does not pretend to be XCTest or an iOS UI test.
import Foundation
import CryptoKit
@testable import QuestCore

struct Failure: Error { let message: String }
var groups = 0
func check(_ condition: @autoclosure () throws -> Bool, _ message: String) throws {
    if try !condition() { throw Failure(message: message) }
}
func rejects(_ expected: SaveError? = nil, _ action: () throws -> Void) throws {
    do { try action() } catch {
        if let expected { try check(error as? SaveError == expected, "Wrong error: \(error)") }
        return
    }
    throw Failure(message: "Expected failure did not occur")
}
func test(_ name: String, _ body: () throws -> Void) throws {
    try body(); groups += 1; print("PASS \(name)")
}
func temporary(_ body: (URL) throws -> Void) throws {
    let directory = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
    try FileManager.default.createDirectory(at: directory, withIntermediateDirectories: true)
    defer { try? FileManager.default.removeItem(at: directory) }
    try body(directory)
}
let root = URL(fileURLWithPath: CommandLine.arguments[1])

try test("8,206 golden comparisons with the unchanged JavaScript engine") {
    struct Fixtures: Decodable {
        struct Case: Decodable { let load: [Int]; let delivered: [Int]; let capacity: Int; let expected: CargoCheck }
        let cases: [Case]
    }
    let data = try Data(contentsOf: root.appendingPathComponent("fixtures/cargo-contract.json"))
    let fixtures = try JSONDecoder().decode(Fixtures.self, from: data)
    try check(fixtures.cases.count == 8206, "Fixture count")
    for (index, item) in fixtures.cases.enumerated() {
        try check(CargoRules.check(load: item.load, delivered: item.delivered, capacity: item.capacity) == item.expected, "Golden mismatch \(index)")
    }
}
try test("Independent exhaustive search: explorer 2 trips, engineer 3 trips") {
    let weights = [7, 6, 4, 3, 2, 2]
    for mode in Difficulty.allCases {
        var queue: [(Int, [[Int]])] = [(0, [])], seen: Set<Int> = [0]
        var cursor = 0, solution: [[Int]]?
        while cursor < queue.count {
            let (arrived, trips) = queue[cursor]; cursor += 1
            if arrived == 63 { solution = trips; break }
            for mask in 1..<64 where mask & arrived == 0 {
                let load = (0..<6).filter { mask & (1 << $0) != 0 }
                if load.reduce(0, { $0 + weights[$1] }) > (mode == .engineer ? 10 : 12) { continue }
                if mask & 2 != 0 && arrived & 1 == 0 { continue }
                if mask & 4 != 0 && mask & 8 != 0 { continue }
                if seen.insert(arrived | mask).inserted { queue.append((arrived | mask, trips + [load])) }
            }
        }
        try check(solution?.count == (mode == .engineer ? 3 : 2), "Shortest solution")
        var game = CargoState()
        for trip in solution ?? [] {
            trip.forEach { game.toggle($0) }
            try check(game.launch(mode).ok, "Reducer rejected independently valid solution")
        }
        try check(game.done && game.isValid(for: mode), "Solved state")
    }
}
try test("Rejected moves preserve selections; undo reopens completion; restart clears one game") {
    var game = CargoState(); game.toggle(1)
    try check(game.launch(.engineer).reason == .crane && game.load == [1] && game.rejected == 1, "Rejection")
    game.toggle(1)
    for trip in [[0, 3], [1, 2], [4, 5]] {
        trip.forEach { game.toggle($0) }; try check(game.launch(.engineer).ok, "Voyage")
    }
    try check(game.done, "Completed")
    game.undo()
    try check(!game.done && game.load.isEmpty && game.delivered == [0, 3, 1, 2], "Undo")
    game = CargoState()
    try check(game.trips.isEmpty && game.rejected == 0, "Restart")
}
try test("Engineer trip budget, explorer unlimited, invalid selectors and hint bounds") {
    var game = CargoState()
    for id in [0, 1, 2] { game.toggle(id); try check(game.launch(.engineer).ok, "First three") }
    game.toggle(3)
    try check(game.launch(.engineer).reason == .voyages && game.load == [3], "Budget")
    game.undo(); try check(game.trips.count == 2 && game.load.isEmpty, "Budget recovery")
    game = CargoState()
    [-1, 6, Int.max].forEach { game.toggle($0) }
    try check(game.load.isEmpty, "Invalid selection")
    for _ in 0..<10 { game.hint() }
    try check(game.hints == 3, "Hints")
    for id in 0..<6 { game.toggle(id); try check(game.launch(.explorer).ok, "Explorer voyage") }
    try check(game.done, "Six single voyages")
}
try test("Invalid persisted histories are rejected before use") {
    for json in [
        #"{"load":[],"trips":[[1],[0]],"rejected":0,"hints":0}"#,
        #"{"load":[0],"trips":[[0]],"rejected":0,"hints":0}"#,
        #"{"load":[0,0],"trips":[],"rejected":0,"hints":0}"#,
        #"{"load":[],"trips":[[0],[0]],"rejected":0,"hints":0}"#,
        #"{"load":[],"trips":[],"rejected":-1,"hints":0}"#,
        #"{"load":[],"trips":[[0],[1],[2],[3]],"rejected":0,"hints":0}"#
    ] {
        let game = try JSONDecoder().decode(CargoState.self, from: Data(json.utf8))
        try check(!game.isValid(for: .engineer), "Invalid rule state")
    }
}
try test("Real disk reopen preserves 2 profiles × 2 modes, language, route, motion and selection") {
    try temporary { directory in
        var p = Progress(); p.active.cargo.toggle(0); p.active.cargo.toggle(3)
        _ = p.active.cargo.launch(.explorer)
        p.active.mode = .engineer; p.active.cargo.toggle(2); p.active.destination = .cargo
        p.activeAvatar = .comet; p.active.cargo.toggle(4)
        p.language = .zh; p.motion = false
        try SaveStore(directory: directory).save(p)
        var restored = try SaveStore(directory: directory).load().progress
        try check(restored == p && restored.active.cargo.load == [4], "Disk roundtrip")
        restored.activeAvatar = .fern
        try check(restored.active.cargo.load == [2] && restored.active.destination == .cargo, "Profile isolation")
        restored.active.mode = .explorer
        try check(restored.active.cargo.trips == [[0, 3]], "Mode isolation")
        restored.active.cargo = CargoState()
        try check(restored.profiles[1].cargo.load == [4] && restored.active.engineer.load == [2], "Scoped restart")
    }
}
try test("Corrupt latest checkpoint recovers previous checkpoint and repairs on next save") {
    try temporary { directory in
        let store = SaveStore(directory: directory); let old = Progress()
        try store.save(old)
        var next = old; next.active.cargo.toggle(0); try store.save(next)
        try Data("broken".utf8).write(to: directory.appendingPathComponent("checkpoint-1.json"))
        try check(store.load().progress == old && store.load().recovered, "Recovery")
        try store.save(next)
        try check(store.load().progress == next && !store.load().recovered, "Repair")
    }
}
try test("Injected partial write and out-of-space error preserve last valid checkpoint") {
    try temporary { directory in
        var old = Progress(); old.active.cargo.toggle(0)
        try SaveStore(directory: directory).save(old)
        let failing = SaveStore(directory: directory) { _, url in
            try Data("partial".utf8).write(to: url); throw CocoaError(.fileWriteOutOfSpace)
        }
        var next = old; next.active.cargo.toggle(3)
        try rejects { try failing.save(next) }
        let recovered = try SaveStore(directory: directory).load()
        try check(recovered.progress == old && recovered.recovered, "Interrupted write recovery")
    }
}
try test("Uncommitted staging file is ignored") {
    try temporary { directory in
        let store = SaveStore(directory: directory); let p = Progress(); try store.save(p)
        try Data("partial".utf8).write(to: directory.appendingPathComponent(".checkpoint.tmp"))
        try check(store.load().progress == p, "Staging file")
    }
}
try test("Both damaged checkpoints block writes and preserve bytes") {
    try temporary { directory in
        for slot in 0...1 { try Data("broken".utf8).write(to: directory.appendingPathComponent("checkpoint-\(slot).json")) }
        let store = SaveStore(directory: directory)
        try rejects(.noRecoverableSave) { _ = try store.load() }
        try rejects(.noRecoverableSave) { try store.save(Progress()) }
        for slot in 0...1 { try check(String(contentsOf: directory.appendingPathComponent("checkpoint-\(slot).json"), encoding: .utf8) == "broken", "Bytes preserved") }
    }
}
try test("Future schema blocks fallback to older data and cannot be overwritten") {
    try temporary { directory in
        let store = SaveStore(directory: directory); try store.save(Progress())
        try Data(#"{"version":2}"#.utf8).write(to: directory.appendingPathComponent("checkpoint-1.json"))
        try rejects(.newerVersion) { _ = try store.load() }
        try rejects(.newerVersion) { try store.save(Progress()) }
    }
}
try test("Checksum covers generation as well as payload; invalid profile set cannot be saved") {
    try temporary { directory in
        let store = SaveStore(directory: directory); let p = Progress()
        try store.save(p); try store.save(p)
        let file = directory.appendingPathComponent("checkpoint-1.json")
        var envelope = try JSONSerialization.jsonObject(with: Data(contentsOf: file)) as! [String: Any]
        envelope["generation"] = 9000
        try JSONSerialization.data(withJSONObject: envelope).write(to: file)
        try check(store.load().recovered, "Checksum")
        var bad = p; bad.profiles.removeLast()
        try rejects(.invalidState) { try store.save(bad) }
    }
}
try test("Changed content revision requires migration and preserves the save") {
    try temporary { directory in
        let store = SaveStore(directory: directory); try store.save(Progress())
        let file = directory.appendingPathComponent("checkpoint-0.json")
        var envelope = try JSONSerialization.jsonObject(with: Data(contentsOf: file)) as! [String: Any]
        let data = Data(base64Encoded: envelope["payload"] as! String)!
        var payload = try JSONSerialization.jsonObject(with: data) as! [String: Any]
        payload["contentChecksum"] = "old-content"
        let changed = try JSONSerialization.data(withJSONObject: payload)
        envelope["payload"] = changed.base64EncodedString()
        envelope["checksum"] = SHA256.hash(data: Data("1:1:".utf8) + changed).map { String(format: "%02x", $0) }.joined()
        try JSONSerialization.data(withJSONObject: envelope).write(to: file)
        try rejects(.changedContent) { _ = try store.load() }
    }
}
try test("Permission failure before write leaves previous checkpoint untouched") {
    try temporary { directory in
        let p = Progress(); try SaveStore(directory: directory).save(p)
        let file = directory.appendingPathComponent("checkpoint-0.json")
        let bytes = try Data(contentsOf: file)
        let store = SaveStore(directory: directory) { _, _ in throw CocoaError(.fileWriteNoPermission) }
        try rejects { try store.save(p) }
        try check(Data(contentsOf: file) == bytes, "File unchanged")
    }
}
print("PASS: \(groups) standalone Swift verification groups. Not XCTest, iOS build or simulator evidence.")
