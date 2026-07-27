import Foundation

enum PlayerMark: String, Codable, Hashable, CaseIterable {
    case x = "X"
    case o = "O"
    
    var opposite: PlayerMark { self == .x ? .o : .x }
}

enum CellState: Equatable, Codable {
    case empty
    case filled(PlayerMark)
}

enum GameMode: Codable, Hashable {
    case vsComputer(difficulty: AIDifficulty)
    case twoPlayers
}

enum AIDifficulty: String, Codable, Hashable, CaseIterable {
    case easy
    case medium
    case hard
}

struct GameConfig: Hashable, Codable {
    let humanPlays: PlayerMark
    let mode: GameMode
}

enum GameStatus: Equatable {
    case inProgress(currentTurn: PlayerMark)
    case win(winner: PlayerMark, winningLine: [Int])
    case tie
}

struct Board {
    var cells: [CellState] = Array(repeating: .empty, count: 9)
    
    static let winningLines: [[Int]] = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    
    func isFull() -> Bool {
        return !cells.contains { if case .empty = $0 { return true } else { return false } }
    }
    
    func availableMoves() -> [Int] {
        cells.enumerated().compactMap { idx, cell in
            if case .empty = cell { return idx } else { return nil }
        }
    }
    
    func checkWin() -> (winner: PlayerMark, line: [Int])? {
        for line in Board.winningLines {
            let states = line.map { cells[$0] }
            if case let .filled(a) = states[0],
               case let .filled(b) = states[1],
               case let .filled(c) = states[2],
               a == b && b == c {
                return (a, line)
            }
        }
        return nil
    }
}

