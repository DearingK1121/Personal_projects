import Combine
import SwiftUI

// Simple title screen with a Play button
struct TitleView: View {
    var onPlay: () -> Void
    var body: some View {
        VStack(spacing: 32) {
            Spacer(minLength: 40)

            Text("Tic Tac Toe")
                .font(.system(size: 48, weight: .heavy, design: .rounded))
                .multilineTextAlignment(.center)
                .padding(.horizontal)

            Spacer(minLength: 20)

            Button(action: { onPlay() }) {
                Text("Play")
                    .font(.system(size: 28, weight: .bold, design: .rounded))
                    .padding(.vertical, 16)
                    .padding(.horizontal, 48)
            }
            .buttonStyle(.borderedProminent)
            .controlSize(.large)

            Spacer()
        }
        .padding()
    }
}

// Simple setup screen to choose who plays first and game mode
struct SetupView: View {
    var onConfigured: (GameConfig) -> Void
    @State private var firstPlayer: PlayerMark = .x
    @State private var mode: GameMode = .twoPlayers
    var body: some View {
        Form {
            Picker("First Player", selection: $firstPlayer) {
                ForEach(PlayerMark.allCases, id: \.self) { mark in
                    Text(mark.rawValue).tag(mark)
                }
            }
            Picker("Mode", selection: $mode) {
                Text("Two Players").tag(GameMode.twoPlayers)
                ForEach(AIDifficulty.allCases, id: \.self) { diff in
                    Text("CPU - \(diff.rawValue.capitalized)").tag(GameMode.vsComputer(difficulty: diff))
                }
            }
            Button("Start Game") {
                onConfigured(GameConfig(humanPlays: firstPlayer, mode: mode))
            }
        }
        .navigationTitle("Setup")
    }
}

// Minimal view model placeholder to satisfy references
final class GameViewModel: ObservableObject {
    @Published private(set) var board: [CellState] = Array(repeating: .empty, count: 9)
    @Published private(set) var status: GameStatus = .inProgress(currentTurn: .x)
    let config: GameConfig
    
    private let humanMark: PlayerMark
    private let aiMark: PlayerMark

    init(config: GameConfig) {
        self.config = config
        self.humanMark = config.humanPlays
        self.aiMark = humanMark.opposite
        status = .inProgress(currentTurn: .x)
        
        if isVsComputer(), case .inProgress(let turn) = status, turn == aiMark {
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.3) { [weak self] in
                self?.performAIMoveIfNeeded()
            }
        }
    }

    var currentTurn: PlayerMark {
        if case let .inProgress(turn) = status { return turn }
        // Default when not in progress
        return .x
    }

    func reset() {
        board = Array(repeating: .empty, count: 9)
        status = .inProgress(currentTurn: .x)
        
        if isVsComputer(), case .inProgress(let turn) = status, turn == aiMark {
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.3) { [weak self] in
                self?.performAIMoveIfNeeded()
            }
        }
    }

    func makeMove(at index: Int) {
        guard case .inProgress(let turn) = status else { return }
        guard index >= 0 && index < 9 else { return }
        guard case .empty = board[index] else { return }
        board[index] = .filled(turn)

        if let (winner, line) = checkWin() {
            status = .win(winner: winner, winningLine: line)
            return
        }
        if isBoardFull() {
            status = .tie
            return
        }
        let nextTurn = turn.opposite
        status = .inProgress(currentTurn: nextTurn)
        
        if isVsComputer(), nextTurn == aiMark {
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.3) { [weak self] in
                self?.performAIMoveIfNeeded()
            }
        }
    }

    private func isBoardFull() -> Bool {
        !board.contains { if case .empty = $0 { return true } else { return false } }
    }

    private func checkWin() -> (PlayerMark, [Int])? {
        for line in Board.winningLines {
            let states = line.map { board[$0] }
            if case let .filled(a) = states[0],
               case let .filled(b) = states[1],
               case let .filled(c) = states[2],
               a == b && b == c {
                return (a, line)
            }
        }
        return nil
    }
    
    private func isVsComputer() -> Bool {
        if case .vsComputer = config.mode { return true } else { return false }
    }

    private func performAIMoveIfNeeded() {
        guard isVsComputer(), case .inProgress(let turn) = status, turn == aiMark else { return }
        if let move = chooseAIMove() {
            makeMove(at: move)
        }
    }

    private func chooseAIMove() -> Int? {
        switch config.mode {
        case .vsComputer(let difficulty):
            switch difficulty {
            case .easy:
                return randomMove()
            case .medium:
                return winningMove(for: aiMark) ?? blockMove() ?? randomMove()
            case .hard:
                // Simple prioritization: win > block > center > corner > random
                return winningMove(for: aiMark) ?? blockMove() ?? centerMove() ?? cornerMove() ?? randomMove()
            }
        default:
            return nil
        }
    }

    private func randomMove() -> Int? {
        let available = board.enumerated().compactMap { idx, cell -> Int? in
            if case .empty = cell { return idx } else { return nil }
        }
        return available.randomElement()
    }

    private func blockMove() -> Int? {
        return winningMove(for: humanMark)
    }

    private func centerMove() -> Int? {
        if case .empty = board[4] { return 4 } else { return nil }
    }

    private func cornerMove() -> Int? {
        let corners = [0, 2, 6, 8]
        return corners.first(where: { idx in if case .empty = board[idx] { return true } else { return false } })
    }

    private func winningMove(for mark: PlayerMark) -> Int? {
        for line in Board.winningLines {
            let states = line.map { board[$0] }
            let marks = states.compactMap { state -> PlayerMark? in if case let .filled(m) = state { return m } else { return nil } }
            let empties = line.filter { idx in if case .empty = board[idx] { return true } else { return false } }
            if marks.filter({ $0 == mark }).count == 2 && empties.count == 1 {
                return empties.first
            }
        }
        return nil
    }
}

// Simple game screen placeholder with a back action
struct GameView: View {
    @ObservedObject var viewModel: GameViewModel
    var onExit: () -> Void

    private let columns = Array(repeating: GridItem(.flexible(), spacing: 8), count: 3)

    private var winningInfo: (winner: PlayerMark, line: [Int])? {
        if case let .win(winner, line) = viewModel.status { return (winner, line) }
        return nil
    }

    var body: some View {
        VStack(spacing: 16) {
            // Status
            Text(statusText)
                .font(.headline)

            // 3x3 grid
            LazyVGrid(columns: columns, spacing: 8) {
                ForEach(0..<9, id: \.self) { idx in
                    CellView(
                        state: viewModel.board[idx],
                        highlightColor: winningInfo.flatMap { info in
                            info.line.contains(idx) ? (info.winner == .x ? Color.blue : Color.red) : nil
                        }
                    )
                        .aspectRatio(1, contentMode: .fit)
                        .onTapGesture { viewModel.makeMove(at: idx) }
                }
            }
            .padding(.horizontal)

            HStack {
                Button("Reset") { viewModel.reset() }
                Spacer()
                Button("Back to Title") { onExit() }
            }
            .padding(.horizontal)
        }
        .padding()
        .navigationTitle("Game")
    }

    private var statusText: String {
        switch viewModel.status {
        case .inProgress(let turn):
            return "Turn: \(turn.rawValue)"
        case .win(let winner, _):
            return "Winner: \(winner.rawValue)!"
        case .tie:
            return "It's a tie!"
        }
    }
}

// A simple cell view that shows X/O or empty
private struct CellView: View {
    let state: CellState
    var highlightColor: Color? = nil
    @State private var pulse: Bool = false
    var body: some View {
        ZStack {
            // Always show the tile background
            RoundedRectangle(cornerRadius: 8)
                .fill(Color(.secondarySystemBackground))
            RoundedRectangle(cornerRadius: 8)
                .stroke(Color.secondary, lineWidth: 1)

            if let glow = highlightColor {
                RoundedRectangle(cornerRadius: 8)
                    .stroke(glow.opacity(0.9), lineWidth: 3)
                    .scaleEffect(pulse ? 1.04 : 1.0)
                    .shadow(color: glow.opacity(pulse ? 0.9 : 0.5), radius: pulse ? 16 : 8, x: 0, y: 0)
                    .shadow(color: glow.opacity(pulse ? 0.6 : 0.3), radius: pulse ? 28 : 16, x: 0, y: 0)
                    .animation(.easeInOut(duration: 0.9).repeatForever(autoreverses: true), value: pulse)
            }

            // Overlay mark if filled
            if case let .filled(mark) = state {
                Text(mark.rawValue)
                    .font(.system(size: 48, weight: .bold, design: .rounded))
                    .foregroundStyle((highlightColor ?? (mark == .x ? Color.blue : Color.red)))
            }
        }
        .contentShape(Rectangle())
        .onAppear {
            if highlightColor != nil { pulse = true }
        }
        .onChange(of: highlightColor) { _, newValue in
            pulse = (newValue != nil)
        }
    }
}

