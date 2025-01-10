from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QApplication, 
                           QPushButton, QSlider, QLabel, QColorDialog, QHBoxLayout, QComboBox, QStackedWidget, QSpinBox)
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import Qt, QTimer, QSize  # Added QSize here
from drawing_modes import DrawingMode
from custom_icons import IconGenerator

class ControlWindow(QMainWindow):
    def __init__(self, canvas_window):
        super().__init__(None, Qt.WindowStaysOnTopHint | Qt.Tool | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.canvas_window = canvas_window
        self.setWindowTitle('Controls')
        
        central_widget = QWidget()
        layout = QHBoxLayout()
        
        # Левая группа (инструменты рисования)
        left_layout = QHBoxLayout()
        btn_size = QSize(30, 30)
        icon_size = QSize(20, 20)
        
        # Загружаем иконки из файлов
        self.icons = {
            'brush': QIcon('icons/brush.png'),
            'polygon': QIcon('icons/polygon.png'),
            'lines': QIcon('icons/lines.png'),
            'notes': QIcon('icons/notes.png'),
            'clear': QIcon('icons/clear.png'),
            'undo': QIcon('icons/undo.png'),
            'redo': QIcon('icons/redo.png'),
            'draw_mode': QIcon('icons/draw_mode.png'),
            'click_through': QIcon('icons/click_through.png')
        }
        
        # Перемещаем все кнопки инструментов в левую группу
        self.toggle_btn = QPushButton()
        self.toggle_btn.setIcon(self.icons['draw_mode'])
        self.toggle_btn.setToolTip('Toggle Drawing Mode')
        self.toggle_btn.clicked.connect(self.toggle_drawing)
        self.toggle_btn.setFixedSize(btn_size)
        left_layout.addWidget(self.toggle_btn)
        
        self.clear_btn = QPushButton()
        self.clear_btn.setIcon(self.icons['clear'])
        self.clear_btn.setToolTip('Clear Canvas')
        self.clear_btn.clicked.connect(self.clear_canvas)
        self.clear_btn.setFixedSize(btn_size)
        left_layout.addWidget(self.clear_btn)
        
        self.undo_btn = QPushButton()
        self.undo_btn.setIcon(self.icons['undo'])
        self.undo_btn.setToolTip('Undo')
        self.undo_btn.clicked.connect(lambda: self.canvas_window.canvas.undo())
        self.undo_btn.setFixedSize(btn_size)
        left_layout.addWidget(self.undo_btn)
        
        self.redo_btn = QPushButton()
        self.redo_btn.setIcon(self.icons['redo'])
        self.redo_btn.setToolTip('Redo')
        self.redo_btn.clicked.connect(lambda: self.canvas_window.canvas.redo())
        self.redo_btn.setFixedSize(btn_size)
        left_layout.addWidget(self.redo_btn)
        
        # Добавляем кнопки режимов
        self.brush_btn = QPushButton()
        self.brush_btn.setIcon(self.icons['brush'])
        self.brush_btn.setToolTip('Brush Mode')
        self.brush_btn.setFixedSize(btn_size)
        self.brush_btn.setCheckable(True)
        self.brush_btn.setChecked(True)
        self.brush_btn.clicked.connect(lambda: self.switch_mode(DrawingMode.BRUSH))
        left_layout.addWidget(self.brush_btn)
        
        self.polygon_btn = QPushButton()
        self.polygon_btn.setIcon(self.icons['polygon'])
        self.polygon_btn.setToolTip('Polygon Mode')
        self.polygon_btn.setFixedSize(btn_size)
        self.polygon_btn.setCheckable(True)
        self.polygon_btn.clicked.connect(lambda: self.switch_mode(DrawingMode.POLYGON))
        left_layout.addWidget(self.polygon_btn)
        
        self.lines_btn = QPushButton()
        self.lines_btn.setIcon(self.icons['lines'])
        self.lines_btn.setToolTip('Lines Mode')
        self.lines_btn.setFixedSize(btn_size)
        self.lines_btn.setCheckable(True)
        self.lines_btn.clicked.connect(lambda: self.switch_mode(DrawingMode.LINES))
        left_layout.addWidget(self.lines_btn)
        
        self.notes_btn = QPushButton()
        self.notes_btn.setIcon(self.icons['notes'])
        self.notes_btn.setToolTip('Notes Mode')
        self.notes_btn.setFixedSize(btn_size)
        self.notes_btn.setCheckable(True)
        self.notes_btn.clicked.connect(lambda: self.switch_mode(DrawingMode.NOTES))
        left_layout.addWidget(self.notes_btn)
        
        # Добавляем слайдеры режимов
        self.sides_slider = QSlider(Qt.Horizontal)
        self.sides_slider.setFixedWidth(60)
        self.sides_slider.setMinimum(3)
        self.sides_slider.setMaximum(12)
        self.sides_slider.setValue(5)
        self.sides_slider.valueChanged.connect(lambda v: self.canvas_window.canvas.set_polygon_sides(v))
        self.sides_slider.hide()  # Скрываем изначально
        left_layout.addWidget(self.sides_slider)
        
        self.line_direction_btn = QPushButton('↕️')
        self.line_direction_btn.setToolTip('Toggle Line Direction')
        self.line_direction_btn.setFixedSize(btn_size)
        self.line_direction_btn.clicked.connect(self.toggle_line_direction)
        self.line_direction_btn.hide()
        left_layout.addWidget(self.line_direction_btn)
        
        self.line_spacing_slider = QSlider(Qt.Horizontal)
        self.line_spacing_slider.setFixedWidth(60)
        self.line_spacing_slider.setMinimum(0)
        self.line_spacing_slider.setMaximum(100)
        self.line_spacing_slider.setValue(0)
        self.line_spacing_slider.valueChanged.connect(
            lambda v: self.canvas_window.canvas.set_line_spacing(v))
        self.line_spacing_slider.hide()
        left_layout.addWidget(self.line_spacing_slider)
        
        layout.addLayout(left_layout)
        
        # Добавляем растягивающийся спейсер между группами
        layout.addStretch()
        
        # Правая группа (настройки и управление окном)
        right_layout = QHBoxLayout()
        
        # Настройки линии в отдельной группе
        line_layout = QHBoxLayout()
        
        width_container = QVBoxLayout()
        self.width_label = QLabel('5')
        self.width_label.setAlignment(Qt.AlignCenter)
        self.width_slider = QSlider(Qt.Horizontal)
        self.width_slider.setObjectName('width_slider')
        self.width_slider.setFixedWidth(60)
        self.width_slider.setMinimum(1)
        self.width_slider.setMaximum(20)
        self.width_slider.setValue(5)
        self.width_slider.valueChanged.connect(self.change_line_width)
        width_container.addWidget(self.width_slider)
        width_container.addWidget(self.width_label)
        line_layout.addLayout(width_container)
        
        opacity_container = QVBoxLayout()
        self.opacity_label = QLabel('255')
        self.opacity_label.setAlignment(Qt.AlignCenter)
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setObjectName('opacity_slider')
        self.opacity_slider.setFixedWidth(60)
        self.opacity_slider.setRange(1, 255)
        self.opacity_slider.setValue(255)
        self.opacity_slider.valueChanged.connect(self.change_opacity)
        opacity_container.addWidget(self.opacity_slider)
        opacity_container.addWidget(self.opacity_label)
        line_layout.addLayout(opacity_container)
        
        self.color_btn = QPushButton()
        self.color_btn.setObjectName('color_btn')  # Для CSS стилей
        self.color_btn.setToolTip('Choose Color')
        self.color_btn.clicked.connect(self.choose_color)
        self.color_btn.setFixedSize(QSize(30, 30))
        self.current_color = QColor(Qt.black)
        self.update_color_button()
        line_layout.addWidget(self.color_btn)
        
        right_layout.addLayout(line_layout)
        
        # Кнопки управления окном
        small_btn_size = QSize(20, 20)
        small_icon_size = QSize(16, 16)
        
        self.minimize_btn = QPushButton()
        self.minimize_btn.setIcon(IconGenerator.create_minimize_icon(small_icon_size))
        self.minimize_btn.setToolTip('Minimize')
        self.minimize_btn.clicked.connect(self.minimize_window)
        self.minimize_btn.setFixedSize(small_btn_size)
        right_layout.addWidget(self.minimize_btn)
        
        self.close_btn = QPushButton()
        self.close_btn.setIcon(IconGenerator.create_close_icon(small_icon_size))
        self.close_btn.setToolTip('Close')
        self.close_btn.clicked.connect(QApplication.quit)
        self.close_btn.setFixedSize(small_btn_size)
        self.close_btn.setStyleSheet('QPushButton { color: red; }')
        right_layout.addWidget(self.close_btn)
        
        layout.addLayout(right_layout)
        
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        # Обновляем размер окна
        self.setFixedSize(600, 50)
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() - 620, 20)
        
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
        self.toggle_btn.setIcon(
            self.icons['draw_mode'] if not self.canvas_window.is_clickthrough 
            else self.icons['click_through']
        )
    
    def change_line_width(self, value):
        self.width_label.setText(str(value))
        self.canvas_window.canvas.pen_width = value

    def change_opacity(self, value):
        self.opacity_label.setText(str(value))
        self.canvas_window.canvas.set_drawing_opacity(value)
    
    def choose_color(self):
        color = QColorDialog.getColor(self.current_color, self)
        if color.isValid():
            self.current_color = color
            self.canvas_window.canvas.pen_color = color
            self.update_color_button()
    
    def update_color_button(self):
        self.color_btn.setStyleSheet(
            f'QPushButton {{ background-color: {self.current_color.name()}; }}'
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

    def toggle_line_direction(self):
        is_vertical = self.line_direction_btn.text() == '↕️'
        self.line_direction_btn.setText('↔️' if is_vertical else '↕️')
        # Исправляем логику: передаем True для вертикальных линий и False для горизонтальных
        self.canvas_window.canvas.set_line_direction(not is_vertical)  # Инвертируем значение

    def switch_mode(self, mode):
        self.canvas_window.canvas.set_drawing_mode(mode)
        # Обновляем состояние кнопок
        self.brush_btn.setChecked(mode == DrawingMode.BRUSH)
        self.polygon_btn.setChecked(mode == DrawingMode.POLYGON)
        self.lines_btn.setChecked(mode == DrawingMode.LINES)
        self.notes_btn.setChecked(mode == DrawingMode.NOTES)
        
        # Показываем/скрываем настройки режимов
        self.sides_slider.setVisible(mode == DrawingMode.POLYGON)
        self.line_direction_btn.setVisible(mode == DrawingMode.LINES)
        self.line_spacing_slider.setVisible(mode == DrawingMode.LINES)
        
        # Обновляем размер окна
        if mode == DrawingMode.POLYGON:
            self.setFixedSize(660, 50)
        elif mode == DrawingMode.LINES:
            self.setFixedSize(700, 50)
        else:
            self.setFixedSize(600, 50)

# Добавляем новый класс для мини-кнопки
class MiniButton(QPushButton):
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Вызываем обработчик клика только для левой кнопки мыши
            super().mousePressEvent(event)
            self.click()  # Эмулируем клик для вызова сигнала clicked
