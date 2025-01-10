// backend/src/board.cpp
#include "board.hpp"
#include <sstream>

Board::Board() : board(BOARD_SIZE, std::vector<Piece>(BOARD_SIZE)) {
    initializeBoard();
}

void Board::initializeBoard() {
    // Set up initial positions
    for (int col = 0; col < BOARD_SIZE; col++) {
        board[0][col] = Piece(PieceColor::BLACK);
        board[BOARD_SIZE-1][col] = Piece(PieceColor::WHITE);
    }
    
    // Initialize middle rows with empty pieces
    for (int row = 1; row < BOARD_SIZE-1; row++) {
        for (int col = 0; col < BOARD_SIZE; col++) {
            board[row][col] = Piece(PieceColor::NONE);
        }
    }
}

bool Board::isValidPosition(const Position& pos) const {
    return pos.row >= 0 && pos.row < BOARD_SIZE && 
           pos.col >= 0 && pos.col < BOARD_SIZE;
}

PieceColor Board::getPieceAt(const Position& pos) const {
    if (!isValidPosition(pos)) return PieceColor::NONE;
    return board[pos.row][pos.col].getColor();
}

bool Board::setPieceAt(const Position& pos, PieceColor color) {
    if (!isValidPosition(pos)) return false;
    board[pos.row][pos.col] = Piece(color);
    return true;
}

bool Board::isPathClear(const Position& from, const Position& to) const {
    if (from.row == to.row) {
        // Horizontal movement
        int start = std::min(from.col, to.col);
        int end = std::max(from.col, to.col);
        for (int col = start + 1; col < end; col++) {
            if (getPieceAt({from.row, col}) != PieceColor::NONE) {
                return false;
            }
        }
    } else if (from.col == to.col) {
        // Vertical movement
        int start = std::min(from.row, to.row);
        int end = std::max(from.row, to.row);
        for (int row = start + 1; row < end; row++) {
            if (getPieceAt({row, from.col}) != PieceColor::NONE) {
                return false;
            }
        }
    }
    return true;
}

bool Board::movePiece(const Position& from, const Position& to) {
    if (!isValidPosition(from) || !isValidPosition(to)) return false;
    
    PieceColor pieceColor = getPieceAt(from);
    if (pieceColor == PieceColor::NONE) return false;
    
    // Check if move is horizontal or vertical
    if (from.row != to.row && from.col != to.col) return false;
    
    if (!isPathClear(from, to)) return false;
    if (getPieceAt(to) != PieceColor::NONE) return false;
    
    setPieceAt(to, pieceColor);
    setPieceAt(from, PieceColor::NONE);
    
    return true;
}

std::vector<Position> Board::getValidMoves(const Position& from) const {
    std::vector<Position> validMoves;
    
    // Перевіряємо, чи позиція валідна і чи є там фігура
    if (!isValidPosition(from) || getPieceAt(from) == PieceColor::NONE) {
        return validMoves;
    }

    // Перевіряємо всі можливі ходи по горизонталі вправо
    for (int col = from.col + 1; col < BOARD_SIZE; col++) {
        Position to{from.row, col};
        if (getPieceAt(to) == PieceColor::NONE && isPathClear(from, to)) {
            validMoves.push_back(to);
        } else {
            break;  // Зупиняємось при першій перешкоді
        }
    }

    // Перевіряємо всі можливі ходи по горизонталі вліво
    for (int col = from.col - 1; col >= 0; col--) {
        Position to{from.row, col};
        if (getPieceAt(to) == PieceColor::NONE && isPathClear(from, to)) {
            validMoves.push_back(to);
        } else {
            break;
        }
    }

    // Перевіряємо всі можливі ходи по вертикалі вниз
    for (int row = from.row + 1; row < BOARD_SIZE; row++) {
        Position to{row, from.col};
        if (getPieceAt(to) == PieceColor::NONE && isPathClear(from, to)) {
            validMoves.push_back(to);
        } else {
            break;
        }
    }

    // Перевіряємо всі можливі ходи по вертикалі вгору
    for (int row = from.row - 1; row >= 0; row--) {
        Position to{row, from.col};
        if (getPieceAt(to) == PieceColor::NONE && isPathClear(from, to)) {
            validMoves.push_back(to);
        } else {
            break;
        }
    }

    return validMoves;
}

std::vector<Position> Board::checkCaptures(const Position& lastMove) {
    std::vector<Position> capturedPositions;
    PieceColor currentColor = getPieceAt(lastMove);
    PieceColor oppositeColor = (currentColor == PieceColor::BLACK) ? 
                               PieceColor::WHITE : PieceColor::BLACK;

    // Check captures in all four directions
    const int directions[][2] = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};
    
    for (const auto& dir : directions) {
        Position checkPos{lastMove.row + dir[0], lastMove.col + dir[1]};
        std::vector<Position> temp;
        
        while (isValidPosition(checkPos) && getPieceAt(checkPos) == oppositeColor) {
            temp.push_back(checkPos);
            checkPos.row += dir[0];
            checkPos.col += dir[1];
        }
        
        if (isValidPosition(checkPos) && getPieceAt(checkPos) == currentColor && !temp.empty()) {
            capturedPositions.insert(capturedPositions.end(), temp.begin(), temp.end());
        }
    }

    return capturedPositions;
}

std::string Board::serialize() const {
    std::stringstream ss;
    ss << "[";
    for (int i = 0; i < BOARD_SIZE; ++i) {
        ss << "[";
        for (int j = 0; j < BOARD_SIZE; ++j) {
            switch (board[i][j].getColor()) {
                case PieceColor::BLACK:
                    ss << "\"B\"";
                    break;
                case PieceColor::WHITE:
                    ss << "\"W\"";
                    break;
                default:
                    ss << "\"E\"";
            }
            if (j < BOARD_SIZE - 1) ss << ",";
        }
        ss << "]";
        if (i < BOARD_SIZE - 1) ss << ",";
    }
    ss << "]";
    return ss.str();
}

bool Board::deserialize(const std::string& data) {
    // Reset board
    board = std::vector<std::vector<Piece>>(BOARD_SIZE, std::vector<Piece>(BOARD_SIZE));
    
    size_t pos = 1; // Skip first '['
    for (int i = 0; i < BOARD_SIZE; ++i) {
        if (data[pos++] != '[') return false;
        
        for (int j = 0; j < BOARD_SIZE; ++j) {
            while (pos < data.length() && (data[pos] == ' ' || data[pos] == '"')) pos++;
            
            if (pos >= data.length()) return false;
            
            char piece = data[pos];
            switch (piece) {
                case 'B':
                    board[i][j] = Piece(PieceColor::BLACK);
                    break;
                case 'W':
                    board[i][j] = Piece(PieceColor::WHITE);
                    break;
                case 'E':
                    board[i][j] = Piece(PieceColor::NONE);
                    break;
                default:
                    return false;
            }
            
            while (pos < data.length() && data[pos] != ',' && data[pos] != ']') pos++;
            if (j < BOARD_SIZE - 1 && data[pos] != ',') return false;
            pos++; // Skip ',' or ']'
        }
        
        if (i < BOARD_SIZE - 1 && data[pos] != ',') return false;
        if (i < BOARD_SIZE - 1) pos++; // Skip ','
    }
    
    return true;
}