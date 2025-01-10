// backend/include/exports.hpp
#pragma once

#ifdef _WIN32
    #define EXPORT __declspec(dllexport)
#else
    #define EXPORT
#endif

#include "game.hpp"
#include "types.hpp"

#ifdef __cplusplus
extern "C" {
#endif

EXPORT void* __stdcall createGame(void);
EXPORT void __stdcall deleteGame(void* game);
EXPORT bool __stdcall makeMove(void* game, int fromRow, int fromCol, int toRow, int toCol);
EXPORT const char* __stdcall getBoardState(void* game);
EXPORT int __stdcall getCurrentPlayer(void* game);
EXPORT bool __stdcall isGameOver(void* game);
EXPORT int __stdcall getBlackCaptured(void* game);
EXPORT int __stdcall getWhiteCaptured(void* game);
EXPORT bool __stdcall saveGame(void* game, const char* filename);
EXPORT bool __stdcall loadGame(void* game, const char* filename);
EXPORT void __stdcall startNewGame(void* game);
// Додаємо новий метод для отримання можливих ходів
EXPORT const char* __stdcall getValidMoves(void* game, int row, int col);

#ifdef __cplusplus
}
#endif