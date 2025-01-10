#pragma once
#include "piece.hpp"
#include <vector>
#include <string>

class Board {
public:
    static const int BOARD_SIZE = 9;
    Board();
    
    bool isValidPosition(const Position& pos) const;
    PieceColor getPieceAt(const Position& pos) const;
    bool setPieceAt(const Position& pos, PieceColor color);
    bool movePiece(const Position& from, const Position& to);
    std::vector<Position> getValidMoves(const Position& from) const;  // Тільки одне оголошення
    std::vector<Position> checkCaptures(const Position& lastMove);
    std::string serialize() const;
    bool deserialize(const std::string& data);
    void initializeBoard();

private:
    std::vector<std::vector<Piece>> board;
    bool isPathClear(const Position& from, const Position& to) const;
};