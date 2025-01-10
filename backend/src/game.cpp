// backend/src/game.cpp
#include "game.hpp"
#include <fstream>
#include <sstream>

Game::Game() : 
    currentPlayer(PieceColor::BLACK),
    blackCaptured(0),
    whiteCaptured(0) {
}

bool Game::makeMove(const Position& from, const Position& to) {
    if (getPieceAt(from) != currentPlayer) return false;
    
    if (!board.movePiece(from, to)) return false;
    
    auto captures = board.checkCaptures(to);
    for (const auto& pos : captures) {
        if (board.getPieceAt(pos) == PieceColor::BLACK) {
            whiteCaptured++;
        } else {
            blackCaptured++;
        }
        board.setPieceAt(pos, PieceColor::NONE);
    }
    
    moveHistory.push_back({from, to});
    switchPlayer();
    return true;
}

void Game::switchPlayer() {
    currentPlayer = (currentPlayer == PieceColor::BLACK) ? 
                    PieceColor::WHITE : PieceColor::BLACK;
}

PieceColor Game::getCurrentPlayer() const {
    return currentPlayer;
}

bool Game::isGameOver() const {
    return blackCaptured >= 9 || whiteCaptured >= 9;
}

int Game::getBlackCaptured() const {
    return blackCaptured;
}

int Game::getWhiteCaptured() const {
    return whiteCaptured;
}

std::string Game::getBoardState() const {
    return board.serialize();
}

bool Game::save(const std::string& filename) const {
    std::ofstream file(filename);
    if (!file.is_open()) return false;
    
    // Format: board_state;current_player;black_captured;white_captured
    file << board.serialize() << ";"
         << (currentPlayer == PieceColor::BLACK ? "B" : "W") << ";"
         << blackCaptured << ";"
         << whiteCaptured;
    
    return true;
}

bool Game::load(const std::string& filename) {
    std::ifstream file(filename);
    if (!file.is_open()) return false;
    
    std::string content;
    std::getline(file, content);
    
    size_t pos1 = content.find(';');
    if (pos1 == std::string::npos) return false;
    
    size_t pos2 = content.find(';', pos1 + 1);
    if (pos2 == std::string::npos) return false;
    
    size_t pos3 = content.find(';', pos2 + 1);
    if (pos3 == std::string::npos) return false;
    
    std::string boardStr = content.substr(0, pos1);
    std::string playerStr = content.substr(pos1 + 1, pos2 - pos1 - 1);
    std::string blackCapStr = content.substr(pos2 + 1, pos3 - pos2 - 1);
    std::string whiteCapStr = content.substr(pos3 + 1);
    
    if (!board.deserialize(boardStr)) return false;
    
    currentPlayer = (playerStr == "B") ? PieceColor::BLACK : PieceColor::WHITE;
    blackCaptured = std::stoi(blackCapStr);
    whiteCaptured = std::stoi(whiteCapStr);
    
    return true;
}

PieceColor Game::getPieceAt(const Position& pos) const {
    return board.getPieceAt(pos);
}

std::vector<Position> Game::getValidMoves(const Position& pos) const {
    // Перевіряємо, чи фігура належить поточному гравцю
    if (board.getPieceAt(pos) != currentPlayer) {
        return std::vector<Position>();
    }
    
    return board.getValidMoves(pos);
}