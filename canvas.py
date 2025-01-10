from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QPen, QColor, QPixmap
from PyQt5.QtCore import Qt, QPoint

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

    def paintEvent(self, event):
        painter = QPainter(self)
        # Рисуем сначала фон, потом слой с рисунком
        painter.drawPixmap(0, 0, self.background)
        painter.drawPixmap(0, 0, self.drawing_layer)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() and Qt.LeftButton and self.drawing:
            painter = QPainter(self.drawing_layer)
            painter.setPen(QPen(self.pen_color, self.pen_width, Qt.SolidLine, Qt.RoundCap))
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False
            # Убираем автоматическое переключение режима

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            QApplication.quit()
        # Добавим очистку по клавише C
        elif event.key() == Qt.Key_C:
            self.drawing_layer.fill(Qt.transparent)
            self.update()
    
    def clear_canvas(self):
        self.drawing_layer.fill(Qt.transparent)
        self.update()
