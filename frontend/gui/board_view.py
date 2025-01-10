from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
from PyQt5.QtCore import Qt, QPoint, QSize, pyqtSignal

class BoardView(QWidget):
    move_made = pyqtSignal(tuple, tuple)  # Сигнал для ходу
    valid_moves_requested = pyqtSignal(tuple)  # Сигнал для запиту можливих ходів

    def __init__(self, parent=None):
        super().__init__(parent)
        self.board_size = 9
        self.cell_size = 60
        self.margin = 40
        self.selected_cell = None
        self.valid_moves = []
        self.board_state = None
        self.setMinimumSize(self.calculate_size())

    def calculate_size(self):
        width = height = 2 * self.margin + self.board_size * self.cell_size
        return QSize(width, height)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Малюємо дошку
        self.draw_board(painter)
        self.draw_grid(painter)
        
        # Малюємо можливі ходи під фігурами
        if self.valid_moves:
            self.draw_valid_moves(painter)
        
        # Малюємо фігури
        if self.board_state:
            self.draw_pieces(painter)
            
        # Малюємо виділення вибраної клітинки
        if self.selected_cell:
            self.draw_selection(painter)
        
    def draw_board(self, painter):
        board_rect = self.rect()
        painter.fillRect(board_rect, QColor(222, 184, 135))
        
    def draw_grid(self, painter):
        pen = QPen(Qt.black, 1)
        painter.setPen(pen)
        
        for i in range(self.board_size + 1):
            # Вертикальні лінії
            x = self.margin + i * self.cell_size
            painter.drawLine(x, self.margin,
                           x, self.margin + self.board_size * self.cell_size)
            
            # Горизонтальні лінії
            y = self.margin + i * self.cell_size
            painter.drawLine(self.margin, y,
                           self.margin + self.board_size * self.cell_size, y)
                           
    def draw_pieces(self, painter):
        for row in range(self.board_size):
            for col in range(self.board_size):
                piece = self.board_state[row][col]
                if piece and piece != 'E':  # Малюємо тільки якщо не порожня клітинка
                    x = self.margin + col * self.cell_size + self.cell_size // 2
                    y = self.margin + row * self.cell_size + self.cell_size // 2
                    radius = self.cell_size // 2 - 5

                    if piece == 'B':
                        color = Qt.black
                        painter.setPen(Qt.NoPen)
                    else:  # piece == 'W'
                        color = Qt.white
                        painter.setPen(QPen(Qt.black, 2))

                    painter.setBrush(QBrush(color))
                    painter.drawEllipse(QPoint(x, y), radius, radius)

    def draw_selection(self, painter):
        row, col = self.selected_cell
        x = self.margin + col * self.cell_size
        y = self.margin + row * self.cell_size
        
        pen = QPen(QColor(255, 0, 0))  # Червоний колір для виділення
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(x, y, self.cell_size, self.cell_size)
                    
    def update_board(self, board_state):
        print("Updating board state")  # Debug print
        if board_state is not None:
            self.board_state = board_state
        self.selected_cell = None
        self.valid_moves = []
        self.update()

    def mousePressEvent(self, event):
        if not self.board_state:
            return
            
        x = event.x() - self.margin
        y = event.y() - self.margin
        
        if x >= 0 and y >= 0:
            col = x // self.cell_size
            row = y // self.cell_size
            
            if col < self.board_size and row < self.board_size:
                print(f"Clicked cell: ({row}, {col})")  # Debug print
                if self.selected_cell is None:
                    # Перевіряємо, чи є фігура в клітинці
                    if self.board_state[row][col] not in ['E', None]:
                        self.selected_cell = (row, col)
                        print(f"Selected cell: {self.selected_cell}")  # Debug print
                        print("Emitting valid_moves_requested signal")  # Debug print
                        self.valid_moves_requested.emit((row, col))
                        self.update()
                else:
                    # Спроба зробити хід
                    from_pos = self.selected_cell
                    to_pos = (row, col)
                    print(f"Attempting move from {from_pos} to {to_pos}")  # Debug print
                    print(f"Valid moves: {self.valid_moves}")  # Debug print
                    if to_pos in self.valid_moves:
                        self.move_made.emit(from_pos, to_pos)
                    else:
                        print("Invalid move: destination not in valid moves")  # Debug print
                    self.selected_cell = None
                    self.valid_moves = []
                    self.update()

    def draw_valid_moves(self, painter):
        print(f"Drawing valid moves: {self.valid_moves}")  # Debug print
        highlight_color = QColor(0, 255, 0, 80)
        painter.setBrush(QBrush(highlight_color))
        painter.setPen(Qt.NoPen)
        
        for row, col in self.valid_moves:
            x = self.margin + col * self.cell_size
            y = self.margin + row * self.cell_size
            painter.drawRect(x, y, self.cell_size, self.cell_size)

    def set_valid_moves(self, moves):
        print(f"Setting valid moves: {moves}")  # Debug print
        self.valid_moves = moves if moves else []
        self.update()