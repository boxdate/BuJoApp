import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit
from PyQt6.QtCore import Qt

class EditableLabel(QWidget):
    def __init__(self, initial_text="Click to edit", parent=None):
        super().__init__(parent)
        self.initial_text = initial_text

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0) # Remove margins for cleaner look

        # QLabel for displaying text
        self.display_label = QLabel(self.initial_text)
        self.display_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        # Make QLabel clickable
        self.display_label.mousePressEvent = self.on_label_clicked

        # QLineEdit for editing text
        self.edit_field = QLineEdit(self.initial_text)
        self.edit_field.hide() # Initially hidden
        self.edit_field.editingFinished.connect(self.on_editing_finished)
        self.edit_field.setContentsMargins(0, 0, 0, 0) # Remove margins for cleaner look

        self.layout.addWidget(self.display_label)
        self.layout.addWidget(self.edit_field)

        self.setFixedSize(200, 30) # Example fixed size for the widget

    def on_label_clicked(self, event):
        # Switch to edit mode
        self.display_label.hide()
        self.edit_field.setText(self.display_label.text()) # Ensure text is synced
        self.edit_field.show()
        self.edit_field.setFocus() # Set focus for immediate typing

    def on_editing_finished(self):
        # Switch back to display mode
        self.display_label.setText(self.edit_field.text())
        self.edit_field.hide()
        self.display_label.show()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Input Field Prototype")
        self.setGeometry(100, 100, 400, 200)

        main_layout = QVBoxLayout(self)

        # Add an instance of EditableLabel
        self.editable_task = EditableLabel("My first task")
        main_layout.addWidget(self.editable_task)

        self.editable_memo = EditableLabel("This is a reflection memo.")
        main_layout.addWidget(self.editable_memo)

        main_layout.addStretch() # Push content to top

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())