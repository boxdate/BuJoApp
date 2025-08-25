import unittest
import tkinter as tk
from unittest.mock import patch, MagicMock
import os
import sys

# Add the project directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../MyProject')))

from bujo_app import BuJoApp, DATA_FILE

class TestBuJoApp(unittest.TestCase):
    def setUp(self):
        """Set up a test environment."""
        self.root = tk.Tk()
        # Hide the main window during tests
        self.root.withdraw()
        self.app = BuJoApp(self.root)
        # Ensure the data file is clean before each test
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)

    def tearDown(self):
        """Clean up after each test."""
        # Ensure the data file is removed after tests
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        self.root.destroy()

    def test_initialization(self):
        """Test if the app initializes correctly."""
        self.assertEqual(self.app.master.title(), "デジタルバレットジャーナル")
        self.assertTrue(self.app.task_entry.winfo_exists())
        self.assertTrue(self.app.add_button.winfo_exists())
        self.assertTrue(self.app.task_listbox.winfo_exists())

    def test_add_task_logic(self):
        """Test the logic of adding a task."""
        # Given
        test_task = "A new task to test"
        self.app.task_entry.insert(0, test_task)

        # When
        self.app.add_task()

        # Then
        # 1. Task should be in the listbox
        tasks_in_listbox = self.app.task_listbox.get(0, tk.END)
        self.assertIn(test_task, tasks_in_listbox)

        # 2. Entry field should be cleared
        self.assertEqual(self.app.task_entry.get(), "")

        # 3. Task should be saved to the file
        self.assertTrue(os.path.exists(DATA_FILE))
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn(test_task, content)

if __name__ == '__main__':
    unittest.main()
