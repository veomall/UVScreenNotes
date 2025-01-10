from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QApplication, 
                           QPushButton, QSlider, QLabel, QColorDialog)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, QTimer

class ControlWindow(QMainWindow):
    def __init__(self, canvas_window):
        super().__init__(None, Qt.WindowStaysOnTopHint | Qt.Tool | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.canvas_window = canvas_window
        self.setWindowTitle('Controls')
        
        central_widget = QWidget()
        layout = QVBoxLayout()
        
        # Кнопки управления
        self.toggle_btn = QPushButton('Disable Drawing')
        self.toggle_btn.clicked.connect(self.toggle_drawing)
        layout.addWidget(self.toggle_btn)
        
        # Кнопка очистки
        self.clear_btn = QPushButton('Clear Canvas')
        self.clear_btn.clicked.connect(self.clear_canvas)
        layout.addWidget(self.clear_btn)
        
        # Настройки линии
        layout.addWidget(QLabel('Line Width:'))
        self.width_slider = QSlider(Qt.Horizontal)
        self.width_slider.setMinimum(1)
        self.width_slider.setMaximum(20)
        self.width_slider.setValue(5)
        self.width_slider.valueChanged.connect(self.change_line_width)
        layout.addWidget(self.width_slider)
        
        # Выбор цвета
        self.color_btn = QPushButton('Choose Color')
        self.color_btn.clicked.connect(self.choose_color)
        layout.addWidget(self.color_btn)
        
        self.current_color = QColor(Qt.black)
        self.update_color_button()
        
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        # Настройки окна
        self.setFixedSize(200, 150)  # Увеличили размер для новой кнопки
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() - 220, 20)
        
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.raise_timer = QTimer(self)
        self.raise_timer.timeout.connect(self.ensure_on_top)
        self.raise_timer.start(100)

    def clear_canvas(self):
        self.canvas_window.canvas.clear_canvas()
    
    def toggle_drawing(self):
        self.canvas_window.toggle_click_through()
        self.toggle_btn.setText('Enable Drawing' if self.canvas_window.is_clickthrough else 'Disable Drawing')
    
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
