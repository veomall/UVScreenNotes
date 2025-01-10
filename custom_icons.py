from PyQt5.QtGui import QPainter, QPainterPath, QColor, QPen, QIcon, QPixmap
from PyQt5.QtCore import Qt, QRect, QSize, QPoint
import math

class IconGenerator:
    @staticmethod
    def create_icon(size, draw_func, color=Qt.white):
        pixmap = QPixmap(size)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(color, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        
        draw_func(painter, pixmap.rect())
        painter.end()
        
        return QIcon(pixmap)

    @staticmethod
    def create_brush_icon(size):
        def draw(painter, rect):
            # Рисуем кисть
            path = QPainterPath()
            path.moveTo(rect.width() * 0.3, rect.height() * 0.2)
            path.lineTo(rect.width() * 0.8, rect.height() * 0.7)
            path.lineTo(rect.width() * 0.7, rect.height() * 0.8)
            path.lineTo(rect.width() * 0.2, rect.height() * 0.3)
            path.closeSubpath()
            painter.drawPath(path)
        
        return IconGenerator.create_icon(size, draw)

    @staticmethod
    def create_polygon_icon(size):
        def draw(painter, rect):
            # Рисуем пятиугольник
            points = []
            center = rect.center()
            radius = min(rect.width(), rect.height()) * 0.35
            for i in range(5):
                angle = (i * 72 + 90) * math.pi / 180  # Начинаем с верхней точки
                x = center.x() + radius * math.cos(angle)
                y = center.y() + radius * math.sin(angle)
                points.append(QPoint(int(x), int(y)))
            
            path = QPainterPath()
            path.moveTo(points[0])
            for i in range(1, 5):
                path.lineTo(points[i])
            path.closeSubpath()
            painter.drawPath(path)
        
        return IconGenerator.create_icon(size, draw)

    @staticmethod
    def create_clear_icon(size):
        def draw(painter, rect):
            # Рисуем корзину
            margin = int(rect.width() * 0.2)
            top = int(rect.height() * 0.2)
            bottom = int(rect.height() * 0.8)
            width = rect.width() - 2 * margin
            
            # Ручка корзины
            painter.drawLine(
                int(rect.width() * 0.35), top,
                int(rect.width() * 0.65), top
            )
            
            # Основание корзины
            path = QPainterPath()
            path.moveTo(margin, top + 3)
            path.lineTo(margin + width, top + 3)
            path.lineTo(int(margin + width * 0.85), bottom)
            path.lineTo(int(margin + width * 0.15), bottom)
            path.closeSubpath()
            painter.drawPath(path)
            
            # Полоски внутри корзины
            for i in range(3):
                x = margin + width * (0.3 + i * 0.2)
                painter.drawLine(
                    int(x), int(top + rect.height() * 0.2),
                    int(x), int(bottom - rect.height() * 0.1)
                )
        
        return IconGenerator.create_icon(size, draw)

    @staticmethod
    def create_undo_icon(size):
        def draw(painter, rect):
            # Рисуем стрелку влево
            path = QPainterPath()
            center_x = rect.width() * 0.5
            center_y = rect.height() * 0.5
            radius = min(rect.width(), rect.height()) * 0.3
            
            path.moveTo(center_x - radius, center_y)
            path.arcTo(center_x - radius, center_y - radius,
                      radius * 2, radius * 2,
                      0, -270)
            
            # Наконечник стрелки
            arrow_size = radius * 0.4
            path.lineTo(center_x - radius - arrow_size, center_y)
            path.lineTo(center_x - radius, center_y + arrow_size)
            path.lineTo(center_x - radius, center_y)
            
            painter.drawPath(path)
        
        return IconGenerator.create_icon(size, draw)

    @staticmethod
    def create_redo_icon(size):
        def draw(painter, rect):
            # Рисуем стрелку вправо (зеркальное отражение undo)
            path = QPainterPath()
            center_x = rect.width() * 0.5
            center_y = rect.height() * 0.5
            radius = min(rect.width(), rect.height()) * 0.3
            
            path.moveTo(center_x + radius, center_y)
            path.arcTo(center_x - radius, center_y - radius,
                      radius * 2, radius * 2,
                      180, 270)
            
            # Наконечник стрелки
            arrow_size = radius * 0.4
            path.lineTo(center_x + radius + arrow_size, center_y)
            path.lineTo(center_x + radius, center_y + arrow_size)
            path.lineTo(center_x + radius, center_y)
            
            painter.drawPath(path)
        
        return IconGenerator.create_icon(size, draw)

    @staticmethod
    def create_lines_icon(size):
        def draw(painter, rect):
            # Рисуем три параллельные линии
            margin = int(rect.width() * 0.2)
            for i in range(3):
                x = int(rect.left() + margin + (rect.width() - 2 * margin) * i / 2)
                y1 = rect.top() + margin
                y2 = rect.bottom() - margin
                painter.drawLine(x, y1, x, y2)
        
        return IconGenerator.create_icon(size, draw)

    @staticmethod
    def create_note_icon(size):
        def draw(painter, rect):
            # Рисуем иконку заметки
            margin = rect.width() * 0.2
            painter.drawRect(int(rect.left() + margin), int(rect.top() + margin),
                           int(rect.width() - 2 * margin), int(rect.height() - 2 * margin))
            # Добавляем линии текста
            line_margin = rect.width() * 0.3
            for i in range(3):
                y = rect.top() + line_margin + (rect.height() - 2 * line_margin) * i / 2
                painter.drawLine(int(rect.left() + line_margin), int(y),
                               int(rect.right() - line_margin), int(y))
        
        return IconGenerator.create_icon(size, draw)

    @staticmethod
    def create_minimize_icon(size):
        def draw(painter, rect):
            margin = int(rect.height() * 0.4)
            painter.drawLine(
                int(rect.left() + 2), 
                int(rect.height() - margin),
                int(rect.right() - 2), 
                int(rect.height() - margin)
            )
        
        return IconGenerator.create_icon(size, draw)

    @staticmethod
    def create_close_icon(size):
        def draw(painter, rect):
            margin = int(rect.width() * 0.2)
            painter.drawLine(
                margin, 
                margin, 
                int(rect.width() - margin), 
                int(rect.height() - margin)
            )
            painter.drawLine(
                margin, 
                int(rect.height() - margin), 
                int(rect.width() - margin), 
                margin
            )
        
        return IconGenerator.create_icon(size, draw, Qt.red)
