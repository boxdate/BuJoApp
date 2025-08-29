import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QFrame
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
        self._setup_styles()

    def _setup_styles(self):
        # Apply styles based on requirements
        # For QLabel (display mode): no border, text looks like handwriting
        self.display_label.setStyleSheet("""
            QLabel {
                border: none;
                font-family: "Comic Sans MS", cursive; /* Placeholder for handwriting font */
                font-size: 14px;
            }
        """)
        # For QLineEdit (edit mode): visible border, text looks like handwriting
        self.edit_field.setStyleSheet("""
            QLineEdit {
                border: 1px solid #888; /* Visible border */
                font-family: "Comic Sans MS", cursive; /* Placeholder for handwriting font */
                font-size: 14px;
            }
        """)

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
        # Set recommended window size
        self.resize(1920, 1080)
        # Set minimum window size
        self.setMinimumSize(1280, 800)

        main_layout = QHBoxLayout(self)

        # Left Page (Yesterday's Reflection)
        self.left_page = QWidget()
        self.left_page.setStyleSheet("background-color: #FDFDF5; border: 1px solid #E0E0D8;") # Light paper color with subtle border
        self.left_page_layout = QVBoxLayout(self.left_page)
        self.left_page_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.left_page_date = QLabel("2025年8月29日 (金)") # Placeholder for date
        self.left_page_date.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.left_page_layout.addWidget(self.left_page_date)

        self.left_page_task = EditableLabel("昨日のタスク")
        self.left_page_layout.addWidget(self.left_page_task)
        self.left_page_layout.addStretch(1) # Push memo down

        self.left_page_memo = EditableLabel("昨日のふりかえりメモ")
        self.left_page_layout.addWidget(self.left_page_memo)

        self.left_page_layout.addStretch(1) # Push content to top

        # Right Page (Today's Record)
        self.right_page = QWidget()
        self.right_page.setStyleSheet("background-color: #FDFDF5; border: 1px solid #E0E0D8;") # Light paper color with subtle border
        self.right_page_layout = QVBoxLayout(self.right_page)
        self.right_page_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.right_page_date = QLabel("2025年8月30日 (土)") # Placeholder for date
        self.right_page_date.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.right_page_layout.addWidget(self.right_page_date)

        self.right_page_task = EditableLabel("今日のタスク")
        self.right_page_layout.addWidget(self.right_page_task)
        self.right_page_layout.addStretch(1) # Push memo down

        self.right_page_memo = EditableLabel("今日のふりかえりメモ")
        self.right_page_layout.addWidget(self.right_page_memo)

        self.right_page_layout.addStretch(1) # Push content to top

        main_layout.addWidget(self.left_page)

        # Add a vertical separator line
        self.separator_line = QFrame()
        self.separator_line.setFrameShape(QFrame.Shape.VLine)
        self.separator_line.setFrameShadow(QFrame.Shadow.Sunken)
        self.separator_line.setLineWidth(2) # Adjust thickness as needed
        main_layout.addWidget(self.separator_line)

        main_layout.addWidget(self.right_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
