import Foundation
import SwiftUI
import QuestCore

@MainActor
final class GameModel: ObservableObject {
    @Published private(set) var progress = QuestCore.Progress()
    @Published private(set) var ready = false
    @Published private(set) var storageIssue: StorageIssue?
    @Published private(set) var feedback: CargoReason?
    @Published private(set) var deliveredNotice = false
    let harbor = HarborScene()
    let island = IslandScene()
    private var store: SaveStore?
    @Published private var systemReducedMotion = false

    enum StorageIssue { case recovered, unavailable, incompatible }
    var profile: Profile { progress.active }
    var cargo: CargoState { profile.cargo }
    var level: CargoLevel { CargoCatalog.bundled.level(profile.mode) }
    var language: Language { progress.language }
    var motion: Bool { progress.motion && !systemReducedMotion }
    func t(_ en: String, _ zh: String) -> String { language == .zh ? zh : en }

    init(store injectedStore: SaveStore? = nil) {
        do {
            if let injectedStore {
                store = injectedStore
            } else {
                let base = try FileManager.default.url(for: .applicationSupportDirectory, in: .userDomainMask,
                                                       appropriateFor: nil, create: true)
                // UI tests get an isolated sandbox folder; production never clears or switches real saves.
                #if DEBUG
                let testRun = ProcessInfo.processInfo.environment["QUESTLY_UI_TEST_RUN"]
                let folder = testRun.map { "Questly-UITests-" + $0.filter { $0.isLetter || $0.isNumber || $0 == "-" } } ?? "Questly"
                #else
                let folder = "Questly"
                #endif
                store = SaveStore(directory: base.appendingPathComponent(folder, isDirectory: true))
            }
            reload()
        } catch { storageIssue = .unavailable }
        harbor.onToggle = { [weak self] id in self?.toggle(id) }
        island.onEnter = { [weak self] in self?.navigate(.cargo) }
        refreshScenes()
    }

    func reload() {
        do {
            guard let store else { storageIssue = .unavailable; return }
            let loaded = try store.load()
            // Ensure even the first session has a durable checkpoint before enabling actions.
            try store.save(loaded.progress)
            progress = loaded.progress
            ready = true
            storageIssue = loaded.recovered ? .recovered : nil
            clearFeedback()
            refreshScenes()
        } catch {
            ready = false
            if let error = error as? SaveError, error == .newerVersion || error == .changedContent {
                storageIssue = .incompatible
            } else { storageIssue = .unavailable }
        }
    }

    @discardableResult
    private func commit(_ edit: (inout QuestCore.Progress) -> Void) -> Bool {
        guard ready, let store else { return false }
        var next = progress
        edit(&next)
        do {
            try store.save(next)
            progress = next
            storageIssue = nil
            refreshScenes()
            return true
        } catch {
            // An I/O error after atomic replacement has an uncertain commit outcome.
            // Freeze editing until explicit reload reconciles disk; never overwrite it
            // with another edit based on the older in-memory state.
            ready = false
            storageIssue = .unavailable
            harbor.cancelPresentation()
            return false
        }
    }

    private func clearFeedback() { feedback = nil; deliveredNotice = false }
    func toggle(_ id: Int) {
        if commit({ $0.active.cargo.toggle(id) }) { clearFeedback() }
    }
    func launch() {
        var result: CargoCheck?
        let loaded = cargo.load
        if commit({ p in
            let mode = p.active.mode
            result = p.active.cargo.launch(mode)
        }), let result {
            feedback = result.reason
            deliveredNotice = result.ok
            if result.ok { harbor.playDelivery(loaded, animated: motion) }
        }
    }
    func undo() { if commit({ $0.active.cargo.undo() }) { clearFeedback() } }
    func restart() { if commit({ $0.active.cargo = CargoState() }) { clearFeedback() } }
    func hint() { _ = commit { $0.active.cargo.hint() } }
    func navigate(_ destination: Destination) {
        if commit({ $0.active.destination = destination }) { clearFeedback() }
    }
    func setMode(_ mode: Difficulty) {
        if commit({ $0.active.mode = mode }) { clearFeedback() }
    }
    func select(_ avatar: Avatar) {
        if commit({ $0.activeAvatar = avatar }) { clearFeedback() }
    }
    func changeLanguage() { _ = commit { $0.language = $0.language == .en ? .zh : .en } }
    func setMotion(_ enabled: Bool) { _ = commit { $0.motion = enabled } }
    func reduceMotion(_ reduced: Bool) { systemReducedMotion = reduced; refreshScenes() }
    func suspend() {
        // Every user action has already been synchronously committed. No background timer writes.
        harbor.cancelPresentation()
        island.removeAllActions()
    }
    func resume() { refreshScenes() }
    private func refreshScenes() {
        harbor.present(cargo, language: language)
        island.present(restored: cargo.done)
    }
}
