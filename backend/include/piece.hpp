#pragma once
#include "types.hpp"

class Piece {
public:
    Piece(PieceColor color = PieceColor::NONE);
    PieceColor getColor() const;
    void setColor(PieceColor newColor);

private:
    PieceColor color;
};