import XCTest
@testable import QuestCore

final class CargoTests: XCTestCase {
    func testAllJavaScriptGoldenCases() throws {
        struct Fixture: Decodable {
            struct Case: Decodable { let load: [Int]; let delivered: [Int]; let capacity: Int; let expected: CargoCheck }
            let cases: [Case]
        }
        let root = URL(fileURLWithPath: #filePath).deletingLastPathComponent().deletingLastPathComponent()
            .deletingLastPathComponent().deletingLastPathComponent().deletingLastPathComponent()
        let fixture = try JSONDecoder().decode(Fixture.self, from: Data(contentsOf: root.appendingPathComponent("fixtures/cargo-contract.json")))
        XCTAssertEqual(fixture.cases.count, 8206)
        for (index, item) in fixture.cases.enumerated() {
            XCTAssertEqual(CargoRules.check(load: item.load, delivered: item.delivered, capacity: item.capacity), item.expected, "Fixture \(index)")
        }
    }

    // Independent constraints and BFS, not CargoRules.check as a solvability oracle.
    func testIndependentShortestSolutions() {
        let weights = [7, 6, 4, 3, 2, 2]
        for mode in Difficulty.allCases {
            let capacity = mode == .engineer ? 10 : 12
            var queue: [(Int, [[Int]])] = [(0, [])]
            var seen: Set<Int> = [0]
            var cursor = 0
            var solution: [[Int]]?
            while cursor < queue.count {
                let (delivered, trips) = queue[cursor]; cursor += 1
                if delivered == 63 { solution = trips; break }
                for mask in 1..<64 where mask & delivered == 0 {
                    let load = (0..<6).filter { mask & (1 << $0) != 0 }
                    if load.reduce(0, { $0 + weights[$1] }) > capacity { continue }
                    if mask & 2 != 0 && delivered & 1 == 0 { continue }
                    if mask & 4 != 0 && mask & 8 != 0 { continue }
                    let next = delivered | mask
                    if seen.insert(next).inserted { queue.append((next, trips + [load])) }
                }
            }
            XCTAssertEqual(solution?.count, mode == .engineer ? 3 : 2)
            var game = CargoState()
            for trip in solution ?? [] {
                trip.forEach { game.toggle($0) }
                XCTAssertTrue(game.launch(mode).ok)
            }
            XCTAssertTrue(game.done)
            XCTAssertTrue(game.isValid(for: mode))
        }
    }

    func testRejectedLoadPreservedUndoAndRestart() {
        var game = CargoState()
        game.toggle(1)
        XCTAssertEqual(game.launch(.engineer).reason, .crane)
        XCTAssertEqual(game.load, [1])
        XCTAssertEqual(game.rejected, 1)
        game.toggle(1); game.toggle(0); game.toggle(3)
        XCTAssertTrue(game.launch(.engineer).ok)
        game.toggle(1); game.toggle(2)
        XCTAssertTrue(game.launch(.engineer).ok)
        game.toggle(4); game.toggle(5)
        XCTAssertTrue(game.launch(.engineer).ok)
        XCTAssertTrue(game.done)
        game.undo()
        XCTAssertFalse(game.done)
        XCTAssertEqual(game.delivered, [0, 3, 1, 2])
        XCTAssertEqual(game.load, [])
        game = CargoState()
        XCTAssertTrue(game.trips.isEmpty)
        XCTAssertEqual(game.rejected, 0)
    }

    func testVoyageLimitIsRecoverableAndExplorerUnlimited() {
        var game = CargoState()
        for id in [0, 1, 2] { game.toggle(id); XCTAssertTrue(game.launch(.engineer).ok) }
        game.toggle(3)
        XCTAssertEqual(game.launch(.engineer).reason, .voyages)
        XCTAssertEqual(game.load, [3])
        game.undo()
        XCTAssertEqual(game.trips.count, 2)
        game = CargoState()
        for id in 0..<6 { game.toggle(id); XCTAssertTrue(game.launch(.explorer).ok) }
        XCTAssertTrue(game.done)
    }

    func testInvalidSelectionAndHintBounds() {
        var game = CargoState()
        [-1, 6, Int.max].forEach { game.toggle($0) }
        XCTAssertTrue(game.load.isEmpty)
        for _ in 0..<10 { game.hint() }
        XCTAssertEqual(game.hints, 3)
        XCTAssertTrue(game.isValid(for: .explorer))
    }

    func testMalformedRuleHistoryRejected() throws {
        for json in [
            #"{"load":[],"trips":[[1],[0]],"rejected":0,"hints":0}"#,
            #"{"load":[0],"trips":[[0]],"rejected":0,"hints":0}"#,
            #"{"load":[0,0],"trips":[],"rejected":0,"hints":0}"#,
            #"{"load":[],"trips":[[0],[0]],"rejected":0,"hints":0}"#,
            #"{"load":[],"trips":[],"rejected":-1,"hints":0}"#,
            #"{"load":[],"trips":[[0],[1],[2],[3]],"rejected":0,"hints":0}"#
        ] {
            let game = try JSONDecoder().decode(CargoState.self, from: Data(json.utf8))
            XCTAssertFalse(game.isValid(for: .engineer))
        }
    }
}
