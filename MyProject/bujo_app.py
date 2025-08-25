import tkinter as tk
from tkinter import messagebox
import os

# データファイル名
DATA_FILE = "tasks.txt"
MAX_TASK_LENGTH = 255

class BuJoApp:
    def __init__(self, master):
        self.master = master
        master.title("デジタルバレットジャーナル")
        # タスク入力フレーム
        self.task_frame = tk.Frame(master)
        self.task_frame.pack(pady=10)

        self.task_entry = tk.Entry(self.task_frame, width=50)
        self.task_entry.pack(side=tk.LEFT, padx=5)
        self.task_entry.bind("<KeyRelease>", self.check_task_length) # 文字数制限のイベントバインド
        self.task_entry.bind("<Return>", self.add_task) # Enterキーでタスク追加

        self.add_button = tk.Button(self.task_frame, text="タスク追加", command=self.add_task)
        self.add_button.pack(side=tk.LEFT, padx=5)

        # タスク表示リスト
        self.task_list_frame = tk.Frame(master)
        self.task_list_frame.pack(pady=10)

        self.task_listbox = tk.Listbox(self.task_list_frame, width=60, height=15)
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.task_list_frame, orient="vertical", command=self.task_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")
        self.task_listbox.config(yscrollcommand=self.scrollbar.set)

        # タスクデータの読み込み
        self.load_tasks()

        # アプリケーション終了時の保存
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def check_task_length(self, event):
        """タスク入力の文字数制限をチェックする"""
        if len(self.task_entry.get()) > MAX_TASK_LENGTH:
            self.task_entry.delete(MAX_TASK_LENGTH, tk.END)
            messagebox.showwarning("文字数制限", f"タスクは{MAX_TASK_LENGTH}文字までに制限されています。")

    def add_task(self, event=None):
        """タスクを追加する"""
        task = self.task_entry.get().strip()
        if task:
            self.task_listbox.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)
            self.save_tasks() # タスク追加時に保存

    def load_tasks(self):
        """ファイルからタスクを読み込む"""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    self.task_listbox.insert(tk.END, line.strip())

    def save_tasks(self):
        """タスクをファイルに保存する"""
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            for i in range(self.task_listbox.size()):
                f.write(self.task_listbox.get(i) + "\n")

    def on_closing(self):
        """アプリケーション終了時の処理"""
        self.save_tasks()
        self.master.destroy()

# アプリケーションの実行
if __name__ == "__main__":
    root = tk.Tk()
    app = BuJoApp(root)
    root.mainloop()
