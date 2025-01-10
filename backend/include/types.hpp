// backend/include/types.hpp
#pragma once
#include <cstdint>
#include <vector>
#include <string>

enum class PieceColor {
    NONE,
    BLACK,
    WHITE
};

// Оператори порівняння для PieceColor
constexpr bool operator==(PieceColor lhs, PieceColor rhs) {
    return static_cast<int>(lhs) == static_cast<int>(rhs);
}

constexpr bool operator!=(PieceColor lhs, PieceColor rhs) {
    return !(lhs == rhs);
}

struct Position {
    int row;
    int col;

    bool operator==(const Position& other) const {
        return row == other.row && col == other.col;
    }
};