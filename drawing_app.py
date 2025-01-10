from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import Qt, QEvent
from canvas import Canvas
from control_window import ControlWindow
import sys

class DrawingApp(QMainWindow):
    def __init__(self):
        super().__init__(None, Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.init_ui()
        
        # Создаем окно управления
        self.control_window = ControlWindow(self)
        self.control_window.show()
        
        # Понижаем z-order холста
        self.lower()
        
        # Добавляем обработчик горячих клавиш
        self.installEventFilter(self)
        
        self.setFocusPolicy(Qt.NoFocus)

    def init_ui(self):
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(screen)
        
        self.canvas = Canvas(self)
        self.setCentralWidget(self.canvas)
        
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.is_clickthrough = False

    def toggle_click_through(self):
        self.is_clickthrough = not self.is_clickthrough
        if self.is_clickthrough:
            self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool | Qt.WindowTransparentForInput)
        else:
            self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        
        self.show()
        self.showFullScreen()
        self.lower()  # Снова понижаем z-order после переключения флагов

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:  # Changed from Qt.KeyPress to QEvent.KeyPress
            # Alt+H для показа/скрытия окна настроек
            if event.key() == Qt.Key_H and event.modifiers() == Qt.AltModifier:
                self.control_window.toggle_visibility()
                return True
        return super().eventFilter(obj, event)

    def focusInEvent(self, event):
        # Игнорируем попытки получения фокуса основным окном
        event.ignore()


def main():
    app = QApplication(sys.argv)
    window = DrawingApp()
    window.showFullScreen()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
