import Foundation
import QuestCore

// Command-line process used by verify-save-crash.sh; never included in the iOS target.
let arguments = CommandLine.arguments
guard arguments.count == 3 else { fatalError("Usage: QuestSaveProbe seed|commit|verify DIRECTORY") }
let directory = URL(fileURLWithPath: arguments[2], isDirectory: true)
let store = SaveStore(directory: directory)
switch arguments[1] {
case "seed":
    var progress = Progress()
    progress.active.mode = .engineer
    progress.active.destination = .cargo
    try store.save(progress)
case "commit":
    var progress = try store.load().progress
    progress.active.cargo.toggle(0); progress.active.cargo.toggle(3)
    precondition(progress.active.cargo.launch(.engineer).ok)
    try store.save(progress)
    try Data("committed".utf8).write(to: directory.appendingPathComponent("ready"), options: .atomic)
    // Stand in for visual playback: state is already durable and independent of this process.
    while true { Thread.sleep(forTimeInterval: 1) }
case "verify":
    let progress = try store.load().progress
    precondition(progress.active.cargo.trips == [[0, 3]])
    precondition(progress.active.cargo.load.isEmpty)
    precondition(progress.active.destination == .cargo)
    precondition(progress.profiles[1].cargo.trips.isEmpty)
    print("PASS: fresh process recovered the committed trip after SIGKILL; other profile remains empty.")
default: fatalError("Unknown command")
}
