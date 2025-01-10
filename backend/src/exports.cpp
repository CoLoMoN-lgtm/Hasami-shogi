// backend/src/exports.cpp
#include "exports.hpp"
#include <string>
#include <sstream>

static std::string lastBoardState;

void* createGame() {
    return new Game();
}

void deleteGame(void* game) {
    delete static_cast<Game*>(game);
}

bool makeMove(void* game, int fromRow, int fromCol, int toRow, int toCol) {
    Game* g = static_cast<Game*>(game);
    Position from{fromRow, fromCol};
    Position to{toRow, toCol};
    return g->makeMove(from, to);
}

const char* getBoardState(void* game) {
    Game* g = static_cast<Game*>(game);
    lastBoardState = g->getBoardState();
    return lastBoardState.c_str();
}

int getCurrentPlayer(void* game) {
    Game* g = static_cast<Game*>(game);
    return static_cast<int>(g->getCurrentPlayer());
}

bool isGameOver(void* game) {
    return static_cast<Game*>(game)->isGameOver();
}

int getBlackCaptured(void* game) {
    return static_cast<Game*>(game)->getBlackCaptured();
}

int getWhiteCaptured(void* game) {
    return static_cast<Game*>(game)->getWhiteCaptured();
}

bool saveGame(void* game, const char* filename) {
    return static_cast<Game*>(game)->save(filename);
}

bool loadGame(void* game, const char* filename) {
    return static_cast<Game*>(game)->load(filename);
}

void startNewGame(void* game) {
    Game* g = static_cast<Game*>(game);
    *g = Game();
}

// Додаємо зберігання останнього результату для valid moves
static std::string lastValidMoves;

const char* __stdcall getValidMoves(void* game, int row, int col) {
    try {
        Game* g = static_cast<Game*>(game);
        Position pos{row, col};
        
        // Отримуємо список можливих ходів
        auto moves = g->getValidMoves(pos);
        
        // Серіалізуємо у простий формат: [row1,col1;row2,col2;...]
        std::stringstream ss;
        ss << "[";
        for (size_t i = 0; i < moves.size(); ++i) {
            if (i > 0) ss << ";";
            ss << moves[i].row << "," << moves[i].col;
        }
        ss << "]";
        
        lastValidMoves = ss.str();
        return lastValidMoves.c_str();
    }
    catch (const std::exception&) {
        lastValidMoves = "[]";
        return lastValidMoves.c_str();
    }
}