from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QApplication, 
                           QPushButton, QSlider, QLabel, QColorDialog, QHBoxLayout)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, QTimer, QSize  # Added QSize here

class ControlWindow(QMainWindow):
    def __init__(self, canvas_window):
        super().__init__(None, Qt.WindowStaysOnTopHint | Qt.Tool | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.canvas_window = canvas_window
        self.setWindowTitle('Controls')
        
        central_widget = QWidget()
        layout = QHBoxLayout()  # Используем горизонтальный layout
        
        # Группа кнопок управления рисованием
        drawing_layout = QHBoxLayout()
        
        # Создаем и настраиваем кнопки с фиксированным размером
        btn_size = QSize(30, 30)
        
        self.toggle_btn = QPushButton('✏️')
        self.toggle_btn.setToolTip('Toggle Drawing Mode')
        self.toggle_btn.clicked.connect(self.toggle_drawing)
        self.toggle_btn.setFixedSize(btn_size)
        drawing_layout.addWidget(self.toggle_btn)
        
        self.clear_btn = QPushButton('🗑️')
        self.clear_btn.setToolTip('Clear Canvas')
        self.clear_btn.clicked.connect(self.clear_canvas)
        self.clear_btn.setFixedSize(btn_size)
        drawing_layout.addWidget(self.clear_btn)
        
        self.undo_btn = QPushButton('↩️')
        self.undo_btn.setToolTip('Undo')
        self.undo_btn.clicked.connect(lambda: self.canvas_window.canvas.undo())
        self.undo_btn.setFixedSize(btn_size)
        drawing_layout.addWidget(self.undo_btn)
        
        self.redo_btn = QPushButton('↪️')
        self.redo_btn.setToolTip('Redo')
        self.redo_btn.clicked.connect(lambda: self.canvas_window.canvas.redo())
        self.redo_btn.setFixedSize(btn_size)
        drawing_layout.addWidget(self.redo_btn)
        
        layout.addLayout(drawing_layout)
        
        # Настройки линии в отдельной группе
        line_layout = QHBoxLayout()
        self.width_slider = QSlider(Qt.Horizontal)
        self.width_slider.setFixedWidth(60)
        self.width_slider.setMinimum(1)
        self.width_slider.setMaximum(20)
        self.width_slider.setValue(5)
        self.width_slider.valueChanged.connect(self.change_line_width)
        line_layout.addWidget(self.width_slider)
        
        # Выбор цвета
        self.color_btn = QPushButton()
        self.color_btn.setToolTip('Choose Color')
        self.color_btn.clicked.connect(self.choose_color)
        self.color_btn.setFixedSize(btn_size)
        self.current_color = QColor(Qt.black)
        self.update_color_button()
        line_layout.addWidget(self.color_btn)
        
        layout.addLayout(line_layout)
        
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        # Настройки окна
        self.setFixedSize(250, 50)
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() - 270, 20)
        
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.raise_timer = QTimer(self)
        self.raise_timer.timeout.connect(self.ensure_on_top)
        self.raise_timer.start(100)

    def clear_canvas(self):
        self.canvas_window.canvas.clear_canvas()
    
    def toggle_drawing(self):
        self.canvas_window.toggle_click_through()
        self.toggle_btn.setText('🎅' if self.canvas_window.is_clickthrough else '✏️')
    
    def change_line_width(self, value):
        self.canvas_window.canvas.pen_width = value
    
    def choose_color(self):
        color = QColorDialog.getColor(self.current_color, self)
        if color.isValid():
            self.current_color = color
            self.canvas_window.canvas.pen_color = color
            self.update_color_button()
    
    def update_color_button(self):
        # Используем value() для получения яркости цвета
        brightness = (self.current_color.red() + self.current_color.green() + self.current_color.blue()) / 3
        self.color_btn.setStyleSheet(
            f'background-color: {self.current_color.name()}; color: {"white" if brightness < 128 else "black"};'
        )
    
    def ensure_on_top(self):
        self.raise_()
        self.activateWindow()
