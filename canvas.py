from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QPen, QColor, QPixmap
from PyQt5.QtCore import Qt, QPoint
from copy import deepcopy
from drawing_modes import DrawingMode
import math

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

        self.drawing_mode = DrawingMode.BRUSH
        self.polygon_sides = 5
        self.polygon_center = None
        self.polygon_radius = 0
        self.polygon_angle = 0

    def set_drawing_mode(self, mode):
        self.drawing_mode = mode

    def set_polygon_sides(self, sides):
        self.polygon_sides = sides
        
    def draw_polygon(self, center, end_point):
        radius = math.sqrt((end_point.x() - center.x())**2 + (end_point.y() - center.y())**2)
        angle = math.atan2(end_point.y() - center.y(), end_point.x() - center.x())
        
        points = []
        for i in range(self.polygon_sides):
            point_angle = angle + (2 * math.pi * i / self.polygon_sides)
            x = center.x() + radius * math.cos(point_angle)
            y = center.y() + radius * math.sin(point_angle)
            points.append(QPoint(int(x), int(y)))
        
        painter = QPainter(self.drawing_layer)
        painter.setPen(QPen(self.pen_color, self.pen_width, Qt.SolidLine, Qt.RoundCap))
        
        # Рисуем полигон
        for i in range(len(points)):
            painter.drawLine(points[i], points[(i + 1) % len(points)])
        
        return points

    def paintEvent(self, event):
        painter = QPainter(self)
        # Рисуем сначала фон, потом слой с рисунком
        painter.drawPixmap(0, 0, self.background)
        painter.drawPixmap(0, 0, self.drawing_layer)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = event.pos()
            if self.drawing_mode == DrawingMode.POLYGON:
                self.polygon_center = event.pos()
            self.current_stroke = []  # Начинаем новый штрих

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton and self.drawing):
            return
            
        if self.drawing_mode == DrawingMode.BRUSH:
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
        elif self.drawing_mode == DrawingMode.POLYGON:
            self.drawing_layer.fill(Qt.transparent)
            self.redraw_from_history()
            points = self.draw_polygon(self.polygon_center, event.pos())
            self.current_stroke = [{
                'mode': DrawingMode.POLYGON,
                'center': self.polygon_center,
                'points': points,
                'color': QColor(self.pen_color),
                'width': self.pen_width,
                'sides': self.polygon_sides
            }]
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
                if all('mode' in line for line in stroke):  # Если это полигон
                    for line in stroke:
                        if line['mode'] == DrawingMode.POLYGON:
                            painter.setPen(QPen(line['color'], line['width'], Qt.SolidLine, Qt.RoundCap))
                            points = line['points']
                            for i in range(len(points)):
                                painter.drawLine(points[i], points[(i + 1) % len(points)])
                else:  # Если это обычные линии
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
