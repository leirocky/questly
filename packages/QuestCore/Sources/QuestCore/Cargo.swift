import Foundation
import CryptoKit

public enum Difficulty: String, Codable, CaseIterable, Sendable { case explorer, engineer }
public enum Language: String, Codable, CaseIterable, Sendable { case en, zh }
public enum Destination: String, Codable, Sendable { case island, cargo }

public struct CargoItem: Codable, Equatable, Sendable, Identifiable {
    public let id: Int
    public let en: String
    public let zh: String
    public let weight: Int
    public let symbol: String
    public func name(_ language: Language) -> String { language == .zh ? zh : en }
}

public struct CargoLevel: Codable, Equatable, Sendable {
    public let mode: Difficulty
    public let capacity: Int
    public let maxTrips: Int?
}

public struct CargoCatalog: Codable, Sendable {
    public let version: Int
    public let id: String
    public let items: [CargoItem]
    public let levels: [CargoLevel]

    // Bundled content is checked by contract tests. A missing bundle is a packaging failure.
    public static let bundled: CargoCatalog = {
        guard let url = Bundle.module.url(forResource: "cargo-v1", withExtension: "json"),
              let data = try? Data(contentsOf: url),
              let catalog = try? JSONDecoder().decode(CargoCatalog.self, from: data),
              catalog.version == 1, catalog.items.map(\.id) == Array(0..<6),
              catalog.items.allSatisfy({ $0.weight > 0 }),
              Set(catalog.levels.map(\.mode)) == Set(Difficulty.allCases) else {
            preconditionFailure("Missing or invalid bundled cargo-v1.json")
        }
        return catalog
    }()

    public static let checksum: String = {
        let encoder = JSONEncoder()
        encoder.outputFormatting = [.sortedKeys]
        return SHA256.hash(data: try! encoder.encode(bundled)).map { String(format: "%02x", $0) }.joined()
    }()

    public func level(_ mode: Difficulty) -> CargoLevel { levels.first { $0.mode == mode }! }
}

public enum CargoReason: String, Codable, Sendable {
    case empty, invalid, unavailable, overweight, crane, water, voyages, complete
}

public struct CargoCheck: Codable, Equatable, Sendable {
    public let ok: Bool
    public let reason: CargoReason?
    public let weight: Int?
    public init(ok: Bool, reason: CargoReason? = nil, weight: Int? = nil) {
        self.ok = ok; self.reason = reason; self.weight = weight
    }
}

public enum CargoRules {
    /// Validation order is the JS cargoCheck contract; selections may be overweight while planning.
    public static func check(load: [Int], delivered: [Int], capacity: Int) -> CargoCheck {
        let items = CargoCatalog.bundled.items
        if load.isEmpty { return CargoCheck(ok: false, reason: .empty) }
        if load.contains(where: { !items.indices.contains($0) }) || Set(load).count != load.count {
            return CargoCheck(ok: false, reason: .invalid)
        }
        if load.contains(where: delivered.contains) { return CargoCheck(ok: false, reason: .unavailable) }
        let weight = load.reduce(0) { $0 + items[$1].weight }
        if weight > capacity { return CargoCheck(ok: false, reason: .overweight, weight: weight) }
        if load.contains(1) && !delivered.contains(0) { return CargoCheck(ok: false, reason: .crane, weight: weight) }
        if load.contains(2) && load.contains(3) { return CargoCheck(ok: false, reason: .water, weight: weight) }
        return CargoCheck(ok: true, weight: weight)
    }
}

public struct CargoState: Codable, Equatable, Sendable {
    public private(set) var load: [Int] = []
    public private(set) var trips: [[Int]] = []
    public private(set) var rejected = 0
    public private(set) var hints = 0
    public init() {}
    public var delivered: [Int] { trips.flatMap { $0 } }
    public var done: Bool { delivered.count == CargoCatalog.bundled.items.count }
    public var weight: Int { load.reduce(0) { $0 + CargoCatalog.bundled.items[$1].weight } }

    public mutating func toggle(_ id: Int) {
        guard !done, CargoCatalog.bundled.items.indices.contains(id), !delivered.contains(id) else { return }
        if load.contains(id) { load.removeAll { $0 == id } } else { load.append(id) }
    }

    @discardableResult public mutating func launch(_ mode: Difficulty) -> CargoCheck {
        guard !done else { return CargoCheck(ok: false, reason: .complete) }
        let level = CargoCatalog.bundled.level(mode)
        if let limit = level.maxTrips, trips.count >= limit { return CargoCheck(ok: false, reason: .voyages) }
        let result = CargoRules.check(load: load, delivered: delivered, capacity: level.capacity)
        guard result.ok else { rejected = min(rejected + 1, 1_000_000); return result }
        trips.append(load)
        load = []
        return result
    }

    public mutating func undo() {
        guard !trips.isEmpty else { return }
        trips.removeLast()
        load = []
    }

    public mutating func hint() { hints = min(hints + 1, 3) }

    public func isValid(for mode: Difficulty) -> Bool {
        let level = CargoCatalog.bundled.level(mode)
        guard trips.count <= (level.maxTrips ?? 6), (0...1_000_000).contains(rejected),
              (0...3).contains(hints), load.count <= 6, Set(load).count == load.count,
              load.allSatisfy({ (0..<6).contains($0) }) else { return false }
        var arrived: [Int] = []
        for trip in trips {
            guard CargoRules.check(load: trip, delivered: arrived, capacity: level.capacity).ok else { return false }
            arrived += trip
        }
        return !load.contains(where: arrived.contains)
    }
}
