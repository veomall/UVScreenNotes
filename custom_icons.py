from PyQt5.QtGui import QPainter, QPen, QIcon, QPixmap
from PyQt5.QtCore import Qt


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
