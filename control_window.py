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
        
        # Добавляем кнопки управления окном в начало
        window_controls = QHBoxLayout()
        btn_size = QSize(20, 20)  # Меньше чем основные кнопки
        
        self.minimize_btn = QPushButton('—')
        self.minimize_btn.setToolTip('Minimize')
        self.minimize_btn.clicked.connect(self.minimize_window)
        self.minimize_btn.setFixedSize(btn_size)
        window_controls.addWidget(self.minimize_btn)
        
        self.close_btn = QPushButton('×')
        self.close_btn.setToolTip('Close')
        self.close_btn.clicked.connect(QApplication.quit)
        self.close_btn.setFixedSize(btn_size)
        self.close_btn.setStyleSheet('QPushButton { color: red; }')
        window_controls.addWidget(self.close_btn)
        
        layout.insertLayout(0, window_controls)
        
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

        # Создаем мини-версию окна
        self.mini_window = MiniButton('🎨', self)
        self.mini_window.setFixedSize(30, 30)
        self.mini_window.clicked.connect(self.restore_window)
        self.mini_window.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Tool | Qt.FramelessWindowHint)
        self.mini_window.hide()

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
        
    def minimize_window(self):
        self.hide()
        self.mini_window.move(10, 10)  # Позиционируем в левом верхнем углу
        self.mini_window.show()
        # Автоматически включаем режим прозрачности для кликов
        if not self.canvas_window.is_clickthrough:
            self.canvas_window.toggle_click_through()
            self.toggle_btn.setText('🎅')
        
    def restore_window(self):
        self.mini_window.hide()
        self.show()
        # Возвращаем режим рисования
        if self.canvas_window.is_clickthrough:
            self.canvas_window.toggle_click_through()
            self.toggle_btn.setText('✏️')
    
    def toggle_visibility(self):
        if self.isVisible():
            self.minimize_window()
        elif self.mini_window.isVisible():
            self.restore_window()
        else:
            self.show()
            # При показе окна возвращаем режим рисования
            if self.canvas_window.is_clickthrough:
                self.canvas_window.toggle_click_through()
                self.toggle_btn.setText('✏️')

# Добавляем новый класс для мини-кнопки
class MiniButton(QPushButton):
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Вызываем обработчик клика только для левой кнопки мыши
            super().mousePressEvent(event)
            self.click()  # Эмулируем клик для вызова сигнала clicked
