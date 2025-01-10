from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QColor, QPen

class NoteCard(QLabel):
    def __init__(self, text="", pos=None, color=Qt.yellow, opacity=200):
        super().__init__(None)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.dragging = False
        self.offset = QPoint()
        self.bg_color = QColor(color)
        self.bg_color.setAlpha(opacity)
        
        # Настраиваем отображение текста
        self.setWordWrap(True)
        self.setMargin(10)
        self.setText(text)
        self.adjustSize()
        
        # Устанавливаем минимальные размеры
        width = max(200, self.sizeHint().width() + 20)
        height = max(100, self.sizeHint().height() + 20)
        self.resize(width, height)
        
        if pos:
            self.move(pos)
        self.show()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Рисуем фон
        painter.setBrush(self.bg_color)
        painter.setPen(QPen(Qt.gray, 1))
        painter.drawRoundedRect(self.rect(), 10, 10)
        
        # Рисуем текст
        text_rect = self.rect().adjusted(10, 10, -10, -10)  # Отступы для текста
        painter.setPen(Qt.black)
        painter.drawText(text_rect, Qt.AlignLeft | Qt.TextWordWrap, self.text())
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos()
            self.raise_()
            self.activateWindow()  # Активируем окно при клике
            
    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(self.mapToParent(event.pos() - self.offset))
            
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
