from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt

class NoteInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Add New Note")
        self.setObjectName("noteDialog")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Enter your note here...")
        layout.addWidget(self.text_edit)
        
        buttons = QHBoxLayout()
        buttons.setSpacing(10)
        
        ok_button = QPushButton("Add")
        ok_button.setDefault(True)
        cancel_button = QPushButton("Cancel")
        
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        
        buttons.addStretch()
        buttons.addWidget(ok_button)
        buttons.addWidget(cancel_button)
        layout.addLayout(buttons)
        
        self.setFixedSize(400, 300)
    
    def get_text(self):
        return self.text_edit.toPlainText()
