import SwiftUI

struct RootView: View {
    @State private var path: [AppRoute] = []
    
    var body: some View {
        NavigationStack(path: $path) {
            TitleView {
                // Navigate to setup when Play is tapped
                path.append(.setup)
            }
            .navigationDestination(for: AppRoute.self) { route in
                switch route {
                case .setup:
                    SetupView { config in
                        path.append(.game(config))
                    }
                case .game(let config):
                    GameView(viewModel: GameViewModel(config: config)) {
                        // When user taps "Back to Title"
                        path = []
                    }
                }
            }
        }
    }
}

enum AppRoute: Hashable {
    case setup
    case game(GameConfig)
}
