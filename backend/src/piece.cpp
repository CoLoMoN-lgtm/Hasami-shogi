#include "piece.hpp"

Piece::Piece(PieceColor color) : color(color) {}

PieceColor Piece::getColor() const {
    return color;
}

void Piece::setColor(PieceColor newColor) {
    color = newColor;
}