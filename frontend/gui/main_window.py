from PyQt5.QtWidgets import (QMainWindow, QAction, QMessageBox, QFileDialog, QLabel,
                             QVBoxLayout, QPushButton, QWidget, QHBoxLayout)
from PyQt5.QtCore import Qt
from .board_view import BoardView
from ..controllers.game_controller import GameController

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.game_controller = GameController()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Хасамі Шогі')
        self.setMinimumSize(1000, 600)

        # Main layout
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        
        # Create board view
        self.board_view = BoardView(self)
        main_layout.addWidget(self.board_view)

        # Create side panel
        self.side_panel = self.create_side_panel()
        main_layout.addLayout(self.side_panel)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Connect signals
        self.board_view.move_made.connect(self.handle_move)
        self.board_view.valid_moves_requested.connect(self.handle_valid_moves_request)

        # Create status bar
        self.status_bar = self.statusBar()
        self.player_label = QLabel("Поточний гравець: Чорний")
        self.status_bar.addWidget(self.player_label)

        self.create_menu()
        self.update_board_state()


    def handle_valid_moves_request(self, position):
        print(f"MainWindow: Handling valid moves request for position: {position}")  # Debug print
        valid_moves = self.game_controller.get_valid_moves(position)
        print(f"MainWindow: Got valid moves: {valid_moves}")  # Debug print
        self.board_view.set_valid_moves(valid_moves)

    
    def create_side_panel(self):
        side_layout = QVBoxLayout()

        # New Game button
        new_game_btn = QPushButton('New Game')
        new_game_btn.clicked.connect(self.new_game)
        side_layout.addWidget(new_game_btn)

        # Exit button
        exit_btn = QPushButton('Exit')
        exit_btn.clicked.connect(self.close)
        side_layout.addWidget(exit_btn)

        side_layout.addStretch()
        return side_layout

    def handle_move(self, from_pos, to_pos):
        print(f"MainWindow: Handling move from {from_pos} to {to_pos}")  # Debug print
        if self.game_controller.make_move(from_pos, to_pos):
            self.update_board_state()
            # Перевіряємо чи гра закінчилась після ходу
            self.check_game_over()
        else:
            self.status_bar.showMessage('Invalid move!', 2000)

    def create_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')

        new_game_action = QAction('New Game', self)
        new_game_action.setShortcut('Ctrl+N')
        new_game_action.triggered.connect(self.new_game)
        file_menu.addAction(new_game_action)

        save_game_action = QAction('Save Game', self)
        save_game_action.setShortcut('Ctrl+S')
        save_game_action.triggered.connect(self.save_game)
        file_menu.addAction(save_game_action)

        load_game_action = QAction('Load Game', self)
        load_game_action.setShortcut('Ctrl+L')
        load_game_action.triggered.connect(self.load_game)
        file_menu.addAction(load_game_action)

        file_menu.addSeparator()

        help_menu = menu_bar.addMenu('Help')

        rules_action = QAction('Rulet', self)
        rules_action.setShortcut('Ctrl+R')
        rules_action.triggered.connect(self.rules)
        file_menu.addAction(rules_action)

        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def new_game(self):
        reply = QMessageBox.question(self, 'Нова гра',
                                   'Чи ви впевнені що хочете запустити нову гру?',
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.game_controller.start_new_game()
            self.update_board_state()

    def save_game(self):
        filename, _ = QFileDialog.getSaveFileName(self,
                                                'Зберегти',
                                                'saves/',
                                                'Hasami Shogi Save (*.hsg)')
        if filename:
            self.game_controller.save_game(filename)
            self.status_bar.showMessage('Game saved successfully', 2000)

    def load_game(self):
        filename, _ = QFileDialog.getOpenFileName(self,
                                                'Завантажити гру',
                                                'saves/',
                                                'Hasami Shogi Save (*.hsg)')
        if filename:
            if self.game_controller.load_game(filename):
                self.update_board_state()
                self.status_bar.showMessage('Game loaded successfully', 2000)
            else:
                QMessageBox.warning(self, 'Error', 'Failed to load game')

    def rules(self):
        rules_text = "Правила:\n 1) На початку гри у гравців по 9 фігур\n 2) Фігуру суперника можна захопити обійшовши її з двох сторін\n 3) Виграє той хто захопить 8 чи бліьше фішур суперника"
        QMessageBox.rules(self, "Правила", rules_text)
        
    def show_about(self):
        about_text = "Hasami Shogi v1.0\nCreated as a coursework project"
        QMessageBox.about(self, 'About', about_text)

    def update_board_state(self):
        board_state = self.game_controller.get_board_state()
        self.board_view.update_board(board_state)
        self.update_status()

    def update_status(self):
        current_player = self.game_controller.get_current_player()
        captures = self.game_controller.get_captures()
        status = f"Current Player: {current_player.capitalize()} | "
        status += f"Captures - Black: {captures['black']}, White: {captures['white']}"
        self.player_label.setText(status)
        
        # Перевіряємо стан гри при кожному оновленні статусу
        if self.game_controller.is_game_over():
            self.check_game_over()

    def check_game_over(self):
        if self.game_controller.is_game_over():
            captures = self.game_controller.get_captures()
            winner = "Black" if captures['white'] >= 9 else "White"
            QMessageBox.information(self, 'Game Over', 
                                  f'Game Over! {winner} wins!\n\n'
                                  f'Captures:\n'
                                  f'Black captured: {captures["black"]} pieces\n'
                                  f'White captured: {captures["white"]} pieces')
            # Можна запропонувати почати нову гру
            reply = QMessageBox.question(self, 'New Game',
                                       'Would you like to start a new game?',
                                       QMessageBox.Yes | QMessageBox.No,
                                       QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.new_game()