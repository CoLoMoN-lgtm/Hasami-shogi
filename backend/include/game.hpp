// backend/include/game.hpp
#pragma once
#include "board.hpp"
#include <vector>
#include <string>

struct Move {
    Position from;
    Position to;
};

class Game {
public:
    Game();
    bool makeMove(const Position& from, const Position& to);
    PieceColor getCurrentPlayer() const;
    bool isGameOver() const;
    int getBlackCaptured() const;
    int getWhiteCaptured() const;
    bool save(const std::string& filename) const;
    bool load(const std::string& filename);
    std::string getBoardState() const;
    PieceColor getPieceAt(const Position& pos) const;
    std::vector<Position> getValidMoves(const Position& pos) const;  // Новий метод

private:
    Board board;
    PieceColor currentPlayer;
    std::vector<Move> moveHistory;
    int blackCaptured;
    int whiteCaptured;
    void switchPlayer();
};