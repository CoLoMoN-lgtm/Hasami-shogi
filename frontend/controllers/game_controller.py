from ..cpp_bridge import GameBridge

class GameController:
    def __init__(self):
        self.game_bridge = GameBridge()
    
    def is_game_over(self):
        """Check if the game is over (9 or more pieces captured)."""
        try:
            captures = self.get_captures()
            return captures['black'] >= 8 or captures['white'] >= 8
        except Exception as e:
            print(f"Error checking game over: {e}")
            return False
        
    def get_winner(self):
        """Get the winner of the game if it's over."""
        captures = self.get_captures()
        if captures['white'] >= 8:
            return 'Black'
        elif captures['black'] >= 8:
            return 'White'
        return None
        
    def get_valid_moves(self, position):
        try:
            print(f"GameController: Getting valid moves for position {position}")  # Debug print
            moves = self.game_bridge.get_valid_moves(position)
            print(f"GameController: Got moves from bridge: {moves}")  # Debug print
            return moves
        except Exception as e:
            print(f"GameController: Error getting valid moves: {e}")  # Debug print
            return []

    def get_board_state(self):
        return self.game_bridge.get_board_state()

    def get_current_player(self):
        return self.game_bridge.get_current_player()

    def get_captures(self):
        return self.game_bridge.get_captures()

    def make_move(self, from_pos, to_pos):
        print(f"GameController: Making move from {from_pos} to {to_pos}")  # Debug print
        return self.game_bridge.make_move(from_pos, to_pos)

    def start_new_game(self):
        self.game_bridge.start_new_game()

    def save_game(self, filename):
        return self.game_bridge.save_game(filename)

    def load_game(self, filename):
        return self.game_bridge.load_game(filename)

