# frontend/cpp_bridge.py
import ctypes
import json
import platform
from pathlib import Path
import os

class GameBridge:
    def __init__(self):
        self._load_library()
        self._setup_function_signatures()
        self.game = self.lib.createGame()
        print("Game instance created")

    def _load_library(self):
        if platform.system() == "Windows":
            lib_name = "hasami_shogi.dll"
        elif platform.system() == "Darwin":
            lib_name = "libhasami_shogi.dylib"
        else:
            lib_name = "libhasami_shogi.so"

        # Додаємо діагностичний вивід
        print("\nLooking for DLL:", lib_name)
        print("Current working directory:", Path.cwd())

        # Розширюємо список можливих шляхів
        possible_paths = [
            Path.cwd() / lib_name,
            Path.cwd() / "backend" / "build" / "Debug" / lib_name,
            Path.cwd() / "backend" / "build" / "Release" / lib_name,
            Path.cwd() / "backend" / "build" / "bin" / lib_name,
            Path.cwd() / "backend" / "build" / "bin" / "Debug" / lib_name,
            Path.cwd() / "backend" / "build" / "bin" / "Release" / lib_name,
            Path(__file__).parent / lib_name,
            Path(__file__).parent.parent / "backend" / "build" / "Debug" / lib_name,
            Path(__file__).parent.parent / "backend" / "build" / "Release" / lib_name,
        ]

        print("\nChecking paths:")
        for path in possible_paths:
            print(f"- {path} (exists: {path.exists()})")

        # Спроба завантажити бібліотеку
        for path in possible_paths:
            if path.exists():
                try:
                    print(f"\nTrying to load: {path}")
                    self.lib = ctypes.CDLL(str(path))
                    print("Successfully loaded!")
                    break
                except Exception as e:
                    print(f"Failed to load {path}: {str(e)}")
                    continue
        else:
            raise RuntimeError(f"Could not find or load {lib_name}")
        pass

    def _setup_function_signatures(self):
        """Setup C++ function signatures."""
        # createGame
        self.lib.createGame.restype = ctypes.c_void_p
        
        # deleteGame
        self.lib.deleteGame.argtypes = [ctypes.c_void_p]
        
        # makeMove
        self.lib.makeMove.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, 
                                     ctypes.c_int, ctypes.c_int]
        self.lib.makeMove.restype = ctypes.c_bool
        
        # getValidMoves
        self.lib.getValidMoves.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
        self.lib.getValidMoves.restype = ctypes.c_char_p
        
        # getBoardState
        self.lib.getBoardState.argtypes = [ctypes.c_void_p]
        self.lib.getBoardState.restype = ctypes.c_char_p
        
        # getCurrentPlayer
        self.lib.getCurrentPlayer.argtypes = [ctypes.c_void_p]
        self.lib.getCurrentPlayer.restype = ctypes.c_int
        
        # isGameOver
        self.lib.isGameOver.argtypes = [ctypes.c_void_p]
        self.lib.isGameOver.restype = ctypes.c_bool
        
        # Captures
        self.lib.getBlackCaptured.argtypes = [ctypes.c_void_p]
        self.lib.getBlackCaptured.restype = ctypes.c_int
        
        self.lib.getWhiteCaptured.argtypes = [ctypes.c_void_p]
        self.lib.getWhiteCaptured.restype = ctypes.c_int
        
        # Game state
        self.lib.saveGame.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        self.lib.saveGame.restype = ctypes.c_bool
        
        self.lib.loadGame.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        self.lib.loadGame.restype = ctypes.c_bool
        
        self.lib.startNewGame.argtypes = [ctypes.c_void_p]

    def create_initial_board(self):
        """Create initial board state if C++ fails to provide one."""
        board = [[None for _ in range(9)] for _ in range(9)]
        # Чорні фігури на першому рядку
        for col in range(9):
            board[0][col] = 'B'
        # Білі фігури на останньому рядку
        for col in range(9):
            board[8][col] = 'W'
        return board

    def get_board_state(self):
        try:
            state_bytes = self.lib.getBoardState(self.game)
            if not state_bytes:
                print("Warning: getBoardState returned None")
                return self.create_initial_board()
            
            state_str = state_bytes.decode('utf-8')
            print("Raw board state:", state_str)  # Debug print
            try:
                board_state = json.loads(state_str)
                return board_state
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                return self.create_initial_board()
        except Exception as e:
            print(f"Error in get_board_state: {e}")
            return self.create_initial_board()

    def make_move(self, from_pos, to_pos):
        """Make a move on the board.
        Args:
            from_pos: tuple (row, col) of starting position
            to_pos: tuple (row, col) of ending position
        Returns:
            bool: True if move was successful
        """
        # Конвертуємо координати в 32-бітні цілі числа
        from_row = ctypes.c_int(from_pos[0])
        from_col = ctypes.c_int(from_pos[1])
        to_row = ctypes.c_int(to_pos[0])
        to_col = ctypes.c_int(to_pos[1])
        
        return self.lib.makeMove(self.game, from_row, from_col, to_row, to_col)

    def get_current_player(self):
        player = self.lib.getCurrentPlayer(self.game)
        return 'black' if player == 1 else 'white'

    def get_captures(self):
        return {
            'black': self.lib.getBlackCaptured(self.game),
            'white': self.lib.getWhiteCaptured(self.game)
        }

    def save_game(self, filename):
        return self.lib.saveGame(self.game, filename.encode('utf-8'))

    def load_game(self, filename):
        return self.lib.loadGame(self.game, filename.encode('utf-8'))

    def start_new_game(self):
        self.lib.startNewGame(self.game)
        print("New game started")  # Debug print

    def __del__(self):
        if hasattr(self, 'lib') and hasattr(self, 'game'):
            self.lib.deleteGame(self.game)

    def get_valid_moves(self, position):
        """Get valid moves for a position.
        Args:
            position: tuple (row, col)
        Returns:
            list of tuples (row, col) representing valid moves
        """
        try:
            # Конвертуємо координати в 32-бітні цілі числа
            row = ctypes.c_int(position[0])
            col = ctypes.c_int(position[1])
            
            # Отримуємо рядок з можливими ходами
            moves_str = self.lib.getValidMoves(self.game, row, col)
            if not moves_str:
                return []
                
            # Декодуємо байти в рядок
            moves_str = moves_str.decode('utf-8')
            print(f"Raw moves string: {moves_str}")  # Debug print
            
            # Парсимо [row1,col1;row2,col2;...]
            if moves_str == "[]":
                return []
                
            moves = []
            # Видаляємо квадратні дужки
            moves_str = moves_str[1:-1]
            if not moves_str:
                return []
                
            # Розбиваємо на окремі ходи
            for move in moves_str.split(';'):
                if ',' in move:
                    r, c = map(int, move.split(','))
                    moves.append((r, c))
            
            return moves
            
        except Exception as e:
            print(f"Error in get_valid_moves: {e}")
            return []