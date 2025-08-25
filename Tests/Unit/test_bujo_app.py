import unittest
import tkinter as tk
from unittest.mock import patch
import os
import sys

# Add the project directory to the Python path to import the app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../MyProject')))

# Given the new instructions, I will assume the app's code will be modified.
# I will import the existing app but my tests will drive its new implementation.
from bujo_app import BuJoApp, DATA_FILE

class TestBuJoApp(unittest.TestCase):
    def setUp(self):
        """Set up a clean environment for each test."""
        # Create a root window for the app, but don't display it
        self.root = tk.Tk()
        self.root.withdraw()

        # In case a previous test failed, ensure the data file is gone
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)

        self.app = BuJoApp(self.root)

    def tearDown(self):
        """Clean up the environment after each test."""
        # Destroy the tkinter window
        self.root.destroy()

        # Clean up the data file
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)

    def test_app_initialization(self):
        """A simple test to ensure the test harness is working."""
        self.assertIsNotNone(self.app)
        self.assertEqual(self.app.master.title(), "デジタルバレットジャーナル")

    def test_add_task_with_button(self):
        """Tests that clicking the 'add' button adds a task to the list."""
        # Given: A task is typed into the entry field
        test_task = "My first task"
        self.app.task_entry.insert(0, test_task)

        # When: The 'add' button is clicked
        self.app.add_button.invoke()

        # Then: The task should appear in the listbox
        tasks_in_listbox = self.app.task_listbox.get(0, tk.END)
        self.assertIn(test_task, tasks_in_listbox)

        # And: The entry field should be cleared
        self.assertEqual(self.app.task_entry.get(), "")

    def test_add_task_with_enter_key(self):
        """Tests that pressing Enter in the entry field adds a task."""
        # Given: A task is typed into the entry field
        test_task = "A task via Enter"
        self.app.task_entry.insert(0, test_task)

        # When: The add_task method is called (simulating the Enter key binding)
        self.app.add_task()

        # Then: The task should appear in the listbox
        tasks_in_listbox = self.app.task_listbox.get(0, tk.END)
        self.assertIn(test_task, tasks_in_listbox)

        # And: The entry field should be cleared
        self.assertEqual(self.app.task_entry.get(), "")

    def test_task_persistence(self):
        """Tests that tasks are saved on closing and loaded on startup."""
        # Given: A task is added to a first instance of the app
        task_to_persist = "This task should be saved"
        self.app.task_entry.insert(0, task_to_persist)
        self.app.add_task()

        # When: The tasks are saved
        self.app.save_tasks()

        # And: The original app window is destroyed to prevent side-effects
        self.root.destroy()

        # And: A new instance of the app is created
        self.root = tk.Tk()
        self.root.withdraw()
        new_app = BuJoApp(self.root)

        # Then: The task should be in the new app's listbox
        tasks_in_new_listbox = new_app.task_listbox.get(0, tk.END)
        self.assertIn(task_to_persist, tasks_in_new_listbox)

    def test_add_empty_task(self):
        """Tests that adding an empty or whitespace task does nothing."""
        # Given: The entry field contains only whitespace
        self.app.task_entry.insert(0, "   ")

        # When: The add_task method is called
        self.app.add_task()

        # Then: The task listbox should still be empty
        self.assertEqual(self.app.task_listbox.size(), 0)

from bujo_app import BuJoApp, DATA_FILE, MAX_TASK_LENGTH

...

    @patch('bujo_app.messagebox')
    def test_character_limit(self, mock_messagebox):
        """Tests that the task entry field enforces a character limit."""
        # Given: A string longer than the max length
        long_string = "a" * (MAX_TASK_LENGTH + 10)

        # When: The long string is inserted
        self.app.task_entry.insert(0, long_string)
        # And: A key release event is triggered
        self.app.task_entry.event_generate("<KeyRelease>")
        self.root.update_idletasks()

        # Then: The entry content should be truncated
        entry_content = self.app.task_entry.get()
        self.assertEqual(len(entry_content), self.app.MAX_TASK_LENGTH)

        # And: A warning message should have been shown
        mock_messagebox.showwarning.assert_called_once()

if __name__ == '__main__':
    # This allows running tests directly from the file
    unittest.main()
