from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit
from PyQt6.QtCore import Qt, QEvent, pyqtSignal # Import pyqtSignal
from PyQt6.QtGui import QKeyEvent

# --- CustomLineEdit (for single-line input with Shift+Enter signal) ---
class CustomLineEdit(QLineEdit):
    shift_enter_pressed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                self.shift_enter_pressed.emit()
                event.accept() # Consume the event
            else:
                super().keyPressEvent(event) # Default QLineEdit behavior for Enter
        else:
            super().keyPressEvent(event)

# --- EditableLabel (for single-line input, e.g., tasks) ---
class EditableLabel(QWidget):
    # Add a signal to EditableLabel to propagate Shift+Enter
    shift_enter_pressed = pyqtSignal() # Signal to emit when Shift+Enter is pressed in edit_field

    def __init__(self, initial_text="Click to edit", parent=None):
        super().__init__(parent)
        self.initial_text = initial_text

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.display_label = QLabel(self.initial_text)
        self.display_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.display_label.mousePressEvent = self.on_label_clicked

        self.edit_field = CustomLineEdit(self) # Use CustomLineEdit
        self.edit_field.hide()
        self.edit_field.editingFinished.connect(self.on_editing_finished)
        self.edit_field.setContentsMargins(0, 0, 0, 0)
        self.edit_field.shift_enter_pressed.connect(self.shift_enter_pressed.emit) # Connect CustomLineEdit's signal

        self.layout.addWidget(self.display_label)
        self.layout.addWidget(self.edit_field)

        self.setMinimumHeight(30) # Keep a minimum height
        self._setup_styles()

    def _setup_styles(self):
        self.display_label.setStyleSheet("""
            QLabel {
                border: none;
                font-family: "Comic Sans MS", cursive;
                font-size: 14px;
            }
        """)
        self.edit_field.setStyleSheet("""
            QLineEdit {
                border: 1px solid #888;
                font-family: "Comic Sans MS", cursive;
                font-size: 14px;
            }
        """)

    def on_label_clicked(self, event):
        self.display_label.hide()
        self.edit_field.setText(self.display_label.text())
        self.edit_field.show()
        self.edit_field.setFocus()

    def on_editing_finished(self):
        self.display_label.setText(self.edit_field.text())
        self.edit_field.hide()
        self.display_label.show()

    def text(self):
        return self.display_label.text()

    def set_text(self, text):
        self.display_label.setText(text)
        self.edit_field.setText(text)

# --- CustomTextEdit (for multi-line input with Enter to finish editing) ---
class CustomTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._editable_label_parent = parent

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                # Shift+Enter: Insert a new line (default QTextEdit behavior)
                super().keyPressEvent(event)
            else:
                # Enter (without Shift): Finish editing
                if self._editable_label_parent and hasattr(self._editable_label_parent, 'on_editing_finished'):
                    self._editable_label_parent.on_editing_finished()
                event.accept()
        else:
            super().keyPressEvent(event)

# --- EditableMultiLineLabel (for multi-line input, e.g., memos) ---
class EditableMultiLineLabel(QWidget):
    def __init__(self, initial_text="Click to edit", parent=None):
        super().__init__(parent)
        self.initial_text = initial_text

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.display_label = QLabel(self.initial_text)
        self.display_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.display_label.mousePressEvent = self.on_label_clicked

        self.edit_field = CustomTextEdit(self) # Use CustomTextEdit
        self.edit_field.hide()
        self.edit_field.setContentsMargins(0, 0, 0, 0)

        self.layout.addWidget(self.display_label)
        self.layout.addWidget(self.edit_field)

        self.setMinimumHeight(30) # Set a minimum height, but allow it to expand
        self._setup_styles()

    def _setup_styles(self):
        self.display_label.setStyleSheet("""
            QLabel {
                border: none;
                font-family: "Comic Sans MS", cursive;
                font-size: 14px;
            }
        """)
        self.edit_field.setStyleSheet("""
            QTextEdit {
                border: 1px solid #888;
                font-family: "Comic Sans MS", cursive;
                font-size: 14px;
            }
        """)

    def on_label_clicked(self, event):
        self.display_label.hide()
        self.edit_field.setPlainText(self.display_label.text())
        self.edit_field.show()
        self.edit_field.setFocus()

    def on_editing_finished(self):
        self.display_label.setText(self.edit_field.toPlainText())
        self.edit_field.hide()
        self.display_label.show()

    def eventFilter(self, obj, event):
        if obj == self.edit_field and event.type() == QEvent.Type.FocusOut:
            # Only call on_editing_finished if focus is lost by other means, not by Enter key
            if not (isinstance(event, QKeyEvent) and (event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter)):
                self.on_editing_finished()
            return True
        return super().eventFilter(obj, event)

    def showEvent(self, event):
        self.edit_field.installEventFilter(self)
        super().showEvent(event)

    def hideEvent(self, event):
        self.edit_field.removeEventFilter(self)
        super().hideEvent(event)

    def text(self):
        return self.display_label.text()

    def set_text(self, text):
        self.display_label.setText(text)
        self.edit_field.setPlainText(text)