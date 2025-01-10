from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QPen, QColor, QPixmap
from PyQt5.QtCore import Qt, QPoint
from copy import deepcopy

class Canvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.drawing = False
        self.last_point = QPoint()
        
        # Настройки рисования
        self.pen_color = QColor(Qt.black)
        self.pen_width = 5
        
        # Создаем два pixmap: один для фона, другой для рисунка
        screen = QApplication.primaryScreen().geometry()
        # Фоновый слой (полупрозрачный)
        self.background = QPixmap(screen.width(), screen.height())
        self.background.fill(QColor(255, 255, 255, 1))  # Очень прозрачный белый
        # Слой для рисования (полностью непрозрачный)
        self.drawing_layer = QPixmap(screen.width(), screen.height())
        self.drawing_layer.fill(Qt.transparent)
        
        self.main_window = None  # Убираем ссылку на главное окно

        self.history = []
        self.redo_stack = []
        self.current_stroke = []

    def paintEvent(self, event):
        painter = QPainter(self)
        # Рисуем сначала фон, потом слой с рисунком
        painter.drawPixmap(0, 0, self.background)
        painter.drawPixmap(0, 0, self.drawing_layer)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = event.pos()
            self.current_stroke = []  # Начинаем новый штрих

    def mouseMoveEvent(self, event):
        if event.buttons() and Qt.LeftButton and self.drawing:
            painter = QPainter(self.drawing_layer)
            painter.setPen(QPen(self.pen_color, self.pen_width, Qt.SolidLine, Qt.RoundCap))
            painter.drawLine(self.last_point, event.pos())
            # Сохраняем точки для истории
            self.current_stroke.append({
                'start': self.last_point,
                'end': event.pos(),
                'color': QColor(self.pen_color),
                'width': self.pen_width
            })
            self.last_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False
            if self.current_stroke:  # Если был штрих
                self.history.append(self.current_stroke)
                self.redo_stack.clear()  # Очищаем стек redo при новом действии

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            QApplication.quit()
        elif event.key() == Qt.Key_C:
            self.clear_canvas()
        elif event.key() == Qt.Key_H and event.modifiers() == Qt.AltModifier:
            # Добавляем обработку Alt+H и здесь
            self.parent().control_window.toggle_visibility()
        self.update()
    
    def undo(self):
        if self.history:
            self.redo_stack.append(self.history.pop())
            self.redraw_from_history()

    def redo(self):
        if self.redo_stack:
            self.history.append(self.redo_stack.pop())
            self.redraw_from_history()

    def redraw_from_history(self):
        self.drawing_layer.fill(Qt.transparent)
        painter = QPainter(self.drawing_layer)
        for stroke in self.history:
            if isinstance(stroke, list):  # Если это штрих
                for line in stroke:
                    painter.setPen(QPen(line['color'], line['width'], Qt.SolidLine, Qt.RoundCap))
                    painter.drawLine(line['start'], line['end'])
        self.update()

    def clear_canvas(self):
        if not self.drawing_layer.isNull():
            # Сохраняем текущее состояние холста перед очисткой
            current_state = []
            # Копируем все штрихи из истории в текущее состояние
            for stroke in self.history:
                if isinstance(stroke, list):
                    current_state.extend(stroke)
            if current_state:  # Если было что сохранять
                self.redo_stack.append(current_state)
            
            self.history.clear()  # Очищаем историю
            self.drawing_layer.fill(Qt.transparent)
            self.update()
