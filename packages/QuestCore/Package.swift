// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "QuestCore",
    platforms: [.iOS(.v17), .macOS(.v13)],
    products: [
        .library(name: "QuestCore", targets: ["QuestCore"]),
        .executable(name: "QuestSaveProbe", targets: ["QuestSaveProbe"])
    ],
    targets: [
        .target(name: "QuestCore", resources: [.process("Resources")]),
        .executableTarget(name: "QuestSaveProbe", dependencies: ["QuestCore"]),
        .testTarget(name: "QuestCoreTests", dependencies: ["QuestCore"])
    ]
)
