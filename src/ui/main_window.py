from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt
from typing import List # Add List for type hinting
from ui.editable_label import EditableLabel, EditableMultiLineLabel

TASK_LIMIT = 7
TASK_HEIGHT = 30 # Example height for a single task line

class MainWindow(QWidget):
    def __init__(self):
        print("MainWindow __init__ started") # Debug print
        super().__init__()
        print("MainWindow super().__init__() called") # Debug print
        self.setWindowTitle("Input Field Prototype")
        # Set recommended window size
        self.resize(1280, 800)
        # Set minimum window size
        self.setMinimumSize(1280, 800)

        main_layout = QHBoxLayout(self)
        print("main_layout created") # Debug print

        # Left Page (Yesterday's Reflection)
        print("Initializing left_page") # Debug print
        self.left_page = QWidget()
        self.left_page.setStyleSheet("""
            background-color: #FDFDF5;
            border-top: 1px solid #E0E0D8;
            border-left: 1px solid #E0E0D8;
            border-bottom: 2px solid #D0D0C8; /* 影の表現 */
            border-right: 2px solid #D0D0C8;  /* 影の表現 */
            border-radius: 8px; /* 角の丸み */
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FDFDF5, stop:0.5 #FCFCF0, stop:1 #FDFDF5); /* ざらつき感の擬似表現 */
        """) # Light paper color with subtle border
        print("left_page stylesheet set") # Debug print
        self.left_page_layout = QVBoxLayout(self.left_page)
        print("left_page_layout created") # Debug print
        self.left_page_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.left_page_date = QLabel("2025年8月29日 (金)") # Placeholder for date
        self.left_page_date.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.left_page_layout.addWidget(self.left_page_date)
        print("left_page_date added") # Debug print

        # Left Page Tasks
        self.left_page_tasks_container_layout = QVBoxLayout()
        print("left_page_tasks_container_layout created") # Debug print
        self.left_page_tasks = []
        for i in range(TASK_LIMIT):
            task_label = EditableLabel(f"昨日のタスク {i+1}")
            print(f"  Task label {i} created") # Debug print inside loop
            task_label.setFixedHeight(TASK_HEIGHT)
            task_label.shift_enter_pressed.connect(lambda idx=i: self._move_focus_to_next_task(idx, self.left_page_tasks))
            self.left_page_tasks_container_layout.addWidget(task_label)
            self.left_page_tasks.append(task_label)
        self.left_page_layout.addLayout(self.left_page_tasks_container_layout)
        print("left_page_tasks_container_layout added to left_page_layout") # Debug print
        self.left_page_layout.addStretch(1) # Push memo down

        # Add a QLabel for the "昨日のふりかえり" title
        yesterday_reflection_title = QLabel("昨日のふりかえり")
        yesterday_reflection_title.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 10px;") # Optional styling
        self.left_page_layout.addWidget(yesterday_reflection_title)

        # EditableMultiLineLabel for the actual reflection content
        self.left_page_memo = EditableMultiLineLabel("ここに昨日のふりかえりを入力...") # Placeholder text
        self.left_page_memo.setFixedHeight(200) # Example fixed height
        self.left_page_layout.addWidget(self.left_page_memo)
        print("left_page_memo added") # Debug print

        self.left_page_layout.addStretch(1) # Push content to top

        # Right Page (Today's Record)
        self.right_page = QWidget()
        print("Initializing right_page") # Debug print
        self.right_page.setStyleSheet("""
            background-color: #FDFDF5;
            border-top: 1px solid #E0E0D8;
            border-left: 1px solid #E0E0D8;
            border-bottom: 2px solid #D0D0C8; /* 影の表現 */
            border-right: 2px solid #D0D0C8;  /* 影の表現 */
            border-radius: 8px; /* 角の丸み */
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FDFDF5, stop:0.5 #FCFCF0, stop:1 #FDFDF5); /* ざらつき感の擬似表現 */
        """) # Light paper color with subtle border
        print("right_page stylesheet set") # Debug print
        self.right_page_layout = QVBoxLayout(self.right_page)
        print("right_page_layout created") # Debug print
        self.right_page_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.right_page_date = QLabel("2025年8月30日 (土)") # Placeholder for date
        self.right_page_date.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.right_page_layout.addWidget(self.right_page_date)
        print("right_page_date added") # Debug print

        # Right Page Tasks
        self.right_page_tasks_container_layout = QVBoxLayout()
        print("right_page_tasks_container_layout created") # Debug print
        self.right_page_tasks = []
        for i in range(TASK_LIMIT):
            task_label = EditableLabel(f"今日のタスク {i+1}")
            print(f"  Right Task label {i} created") # Debug print inside loop
            task_label.setFixedHeight(TASK_HEIGHT)
            task_label.shift_enter_pressed.connect(lambda idx=i: self._move_focus_to_next_task(idx, self.right_page_tasks))
            self.right_page_tasks_container_layout.addWidget(task_label)
            self.right_page_tasks.append(task_label)
        self.right_page_layout.addLayout(self.right_page_tasks_container_layout)
        print("right_page_tasks_container_layout added to right_page_layout") # Debug print
        self.right_page_layout.addStretch(1)

        # Add a QLabel for the "今日のふりかえり" title
        reflection_title = QLabel("今日のふりかえり")
        reflection_title.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 10px;") # Optional styling
        self.right_page_layout.addWidget(reflection_title)

        # EditableMultiLineLabel for the actual reflection content
        self.right_page_memo = EditableMultiLineLabel("ここに今日のふりかえりを入力...") # Placeholder text
        self.right_page_memo.setFixedHeight(200) # Example fixed height
        self.right_page_layout.addWidget(self.right_page_memo)
        print("right_page_memo added") # Debug print

        self.right_page_layout.addStretch(1) # Push content to top

        # These lines should be inside __init__
        print("Adding left_page to main_layout") # Debug print
        main_layout.addWidget(self.left_page)
        print("left_page added") # Debug print

        # Add a vertical separator line
        self.separator_line = QFrame()
        self.separator_line.setFrameShape(QFrame.Shape.VLine)
        self.separator_line.setFrameShadow(QFrame.Shadow.Sunken)
        self.separator_line.setLineWidth(2) # Adjust thickness as needed
        main_layout.addWidget(self.separator_line)
        print("separator_line added") # Debug print

        print("Adding right_page to main_layout") # Debug print
        main_layout.addWidget(self.right_page)
        print("right_page added") # Debug print
        print("MainWindow __init__ finished") # Debug print

    def _move_focus_to_next_task(self, current_task_idx: int, task_list: List[EditableLabel]):
        next_task_idx = current_task_idx + 1
        if next_task_idx < len(task_list):
            task_list[next_task_idx].edit_field.setFocus()
        else:
            # If it's the last task, move focus to the memo field
            if task_list is self.left_page_tasks:
                self.left_page_memo.edit_field.setFocus()
            elif task_list is self.right_page_tasks:
                self.right_page_memo.edit_field.setFocus()
