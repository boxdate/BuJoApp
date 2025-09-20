from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt
from ui.editable_label import EditableLabel

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
