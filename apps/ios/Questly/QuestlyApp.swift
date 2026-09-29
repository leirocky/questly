import SwiftUI

@main
@MainActor
struct QuestlyApp: App {
    @StateObject private var model = GameModel()
    var body: some Scene {
        WindowGroup {
            QuestlyView(model: model)
                .preferredColorScheme(.dark)
        }
    }
}
