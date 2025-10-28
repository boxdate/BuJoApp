import tkinter as tk
from tkinter import messagebox
import os

# データファイル名
DATA_FILE = "tasks.txt"
REFLECTION_FILE = "reflection.txt" # 振り返り用データファイル
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
        self.task_entry.bind("<Return>", self.add_task)

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

        # 振り返り入力フレーム
        self.reflection_frame = tk.Frame(master)
        self.reflection_frame.pack(pady=10)

        self.reflection_label = tk.Label(self.reflection_frame, text="今日の振り返り:")
        self.reflection_label.pack(anchor='w') # ラベルを左寄せで配置

        self.reflection_text = tk.Text(self.reflection_frame, width=60, height=5)
        self.reflection_text.pack(pady=5)

        self.save_reflection_button = tk.Button(self.reflection_frame, text="振り返りを保存", command=self.save_reflection)
        self.save_reflection_button.pack()

        # データの読み込み
        self.load_tasks()
        self.load_reflection()

        # アプリケーション終了時の保存
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def check_task_length(self, event):
        """タスク入力の文字数制限をチェックする"""
        # if len(self.task_entry.get()) > MAX_TASK_LENGTH:
        #     self.task_entry.delete(MAX_TASK_LENGTH, tk.END)
        #     messagebox.showwarning("文字数制限", f"タスクは{MAX_TASK_LENGTH}文字までに制限されています。")
        pass

    def add_task(self, event=None):
        """タスクを追加する"""
        task = self.task_entry.get().strip()
        if task:
            self.task_listbox.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)
            self.save_tasks() # Note: save_tasks will be handled in a later TDD cycle

    def save_reflection(self, show_message=True):
        """振り返りをファイルに保存する"""
        reflection_content = self.reflection_text.get("1.0", tk.END).strip()
        # ファイルが存在しない場合でも、空のファイルが作成される
        with open(REFLECTION_FILE, "w", encoding="utf-8") as f:
            f.write(reflection_content)
        if show_message:
            messagebox.showinfo("保存完了", "振り返りを保存しました。")

    def load_tasks(self):
        """ファイルからタスクを読み込む"""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    self.task_listbox.insert(tk.END, line.strip())

    def load_reflection(self):
        """ファイルから振り返りを読み込む"""
        if os.path.exists(REFLECTION_FILE):
            with open(REFLECTION_FILE, "r", encoding="utf-8") as f:
                reflection_content = f.read()
                self.reflection_text.insert("1.0", reflection_content)

    def save_tasks(self):
        """タスクをファイルに保存する"""
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            for i in range(self.task_listbox.size()):
                f.write(self.task_listbox.get(i) + "\n")

    def on_closing(self):
        """アプリケーション終了時の処理"""
        self.save_tasks()
        self.save_reflection(show_message=False) # メッセージなしで振り返りを保存
        self.master.destroy()

# アプリケーションの実行
if __name__ == "__main__":
    root = tk.Tk()
    app = BuJoApp(root)
    root.mainloop()
