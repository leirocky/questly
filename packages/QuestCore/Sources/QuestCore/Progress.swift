import Foundation

public enum Avatar: String, CaseIterable, Codable, Sendable { case fern, comet }

public struct Profile: Codable, Equatable, Sendable, Identifiable {
    public let id: Avatar
    public var mode: Difficulty = .explorer
    public var destination: Destination = .island
    public var explorer = CargoState()
    public var engineer = CargoState()
    public init(id: Avatar) { self.id = id }
    public var cargo: CargoState {
        get { mode == .explorer ? explorer : engineer }
        set { if mode == .explorer { explorer = newValue } else { engineer = newValue } }
    }
}

public struct Progress: Codable, Equatable, Sendable {
    public let version: Int
    public let contentID: String
    public let contentChecksum: String
    public var activeAvatar: Avatar = .fern
    public var language: Language = .en
    public var motion = true
    public var profiles: [Profile]

    public init() {
        version = 1
        contentID = CargoCatalog.bundled.id
        contentChecksum = CargoCatalog.checksum
        profiles = Avatar.allCases.map(Profile.init)
    }

    public var active: Profile {
        get { profiles.first { $0.id == activeAvatar }! }
        set { if let i = profiles.firstIndex(where: { $0.id == activeAvatar }) { profiles[i] = newValue } }
    }

    public var isValid: Bool {
        version == 1 && contentID == CargoCatalog.bundled.id && contentChecksum == CargoCatalog.checksum &&
        profiles.count == 2 && Set(profiles.map(\.id)) == Set(Avatar.allCases) &&
        profiles.allSatisfy { $0.explorer.isValid(for: .explorer) && $0.engineer.isValid(for: .engineer) }
    }
}
