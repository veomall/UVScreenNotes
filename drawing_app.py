from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import Qt
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


def main():
    app = QApplication(sys.argv)
    window = DrawingApp()
    window.showFullScreen()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
