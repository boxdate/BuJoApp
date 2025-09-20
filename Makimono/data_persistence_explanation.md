# データ永続化の概念と実装について

このドキュメントでは、アプリケーションにおけるデータの永続化（アプリを閉じてもデータが消えないように保存すること）の概念と、その実装方法について、特に初学者の方にも分かりやすく解説します。

私たちが作ろうとしているバレットジャーナルアプリは、ユーザーが入力した「タスク」「イベント」「メモ」といった情報を記憶しておく必要があります。アプリを閉じたら情報が消えてしまうようでは困ります。この「情報を記憶しておく」という部分が「データの永続化」です。

そして、その永続化を実現するために、大きく分けて3つのステップと、それぞれの役割があります。

---

## 1. データモデルの定義 (`src/core/models.py`)

**なぜ必要か？**
アプリが扱う「情報（データ）」の形を、プログラムが理解しやすいように明確に定義するためです。

例えば、バレットジャーナルには「タスク」「イベント」「メモ」など、様々な種類の情報があります。これらをただのバラバラな文字列として扱うのではなく、「タスクには『内容』『期日』『完了したかどうか』という3つの情報がある」「イベントには『タイトル』『日時』『場所』という情報がある」といったように、データの構造をきちんと決めておくことで、プログラムがデータを扱いやすくなります。

**例え話**
レゴブロックに例えると、データモデルは「どのような形のレゴブロックがあるか（四角、丸、屋根の形など）」を定義するようなものです。それぞれのブロックには、色や大きさといった属性があります。この定義があるからこそ、私たちは「四角いブロックを3つ重ねて壁を作る」といった具体的な組み立て（プログラムでの操作）ができるわけです。

**役割**
*   **データの構造化**: アプリケーションが扱う情報の種類と、それぞれの情報が持つ属性（プロパティ）を定義します。
*   **一貫性の確保**: データの形式が統一されるため、プログラムのどこからでも同じ方法でデータにアクセスできます。
*   **可読性の向上**: コードを見たときに、どのようなデータを扱っているのかがすぐに理解できます。

**具体的な内容**
Pythonでは、通常 `class` を使って定義します。

```python
# src/core/models.py に書く内容のイメージ

class Task:
    def __init__(self, content: str, due_date: str = None, completed: bool = False):
        self.content = content       # タスクの内容（例: "牛乳を買う"）
        self.due_date = due_date     # 期日（例: "2025-08-31"）
        self.completed = completed   # 完了したかどうか（True/False）

class Event:
    def __init__(self, title: str, date: str, time: str, location: str = None):
        self.title = title           # イベントのタイトル（例: "会議"）
        self.date = date             # 日付（例: "2025-09-01"）
        self.time = time             # 時間（例: "10:00"）
        self.location = location     # 場所（例: "会議室A"）

class Note:
    def __init__(self, content: str):
        self.content = content       # メモの内容（例: "今日の気づき"）
```

---

## 2. データ永続化のインターフェース定義 (`src/data/repository.py`)

**なぜ必要か？**
アプリの「データ保存方法」を、プログラムの他の部分から隠すためです。

例えば、最初はデータをファイル（JSONファイルなど）に保存するかもしれません。でも、将来的に「もっとたくさんのデータを扱いたいからデータベースに保存しよう」とか、「複数のデバイスでデータを共有したいからクラウドに保存しよう」といった変更をしたくなるかもしれません。

この「インターフェース」を間に挟むことで、保存方法が変わっても、データを実際に使う側のコード（UIやビジネスロジック）を変更する必要がなくなります。

**例え話**
コンセントに例えると、インターフェースは「コンセントの穴の形」を定義するようなものです。家電製品（データを使う側のプログラム）は、コンセントの穴の形に合わせてプラグ（データの保存・読み込み要求）を差し込めば、電気が供給されます。電気がどこから来ているか（火力発電、水力発電など）を知る必要はありません。家電製品は、コンセントの穴の形さえ知っていれば良いのです。

**役割**
*   **抽象化**: データの「保存する」「読み込む」という操作を抽象化し、具体的な実装（ファイルに書くのか、データベースに書くのかなど）から分離します。
*   **柔軟性**: 将来的にデータ保存方法を変更する際に、影響を受けるプログラムの範囲を限定できます。
*   **テスト容易性**: インターフェースを「モック（模擬オブジェクト）」に置き換えることで、実際にファイルを読み書きせずに、データを使う部分のテストができます。

**具体的な内容**
Pythonでは、`abc` モジュール（Abstract Base Classes）を使って抽象基底クラスとして定義することが多いです。

```python
# src/data/repository.py に書く内容のイメージ
from abc import ABC, abstractmethod
from typing import List
from src.core.models import Task, Event, Note # 先ほど定義したデータモデルをインポート

class JournalRepository(ABC): # ABCを継承して抽象クラスであることを示す
    @abstractmethod # このメソッドは必ず実装しなければならないことを示す
    def save_tasks(self, tasks: List[Task]):
        pass # ここには具体的な処理は書かない

    @abstractmethod
    def load_tasks(self) -> List[Task]:
        pass

    # イベントやメモについても同様に save_events, load_events などが定義される
    @abstractmethod
    def save_events(self, events: List[Event]):
        pass

    @abstractmethod
    def load_events(self) -> List[Event]:
        pass

    @abstractmethod
    def save_notes(self, notes: List[Note]):
        pass

    @abstractmethod
    def load_notes(self) -> List[Note]:
        pass
```

---

## 3. ファイル永続化の実装 (`src/data/file_storage.py`)

**なぜ必要か？**
上で定義したインターフェースの「具体的な中身」を実装するためです。ここでは、実際にファイルを読み書きしてデータを保存・読み込みする処理を書きます。

**例え話**
コンセントの例で言うと、これは「実際に電気を供給する発電所」にあたります。コンセントの穴の形（インターフェース）に合わせて、電気を生成し、供給する具体的な方法（火力発電、水力など）を実装します。

**役割**
*   **具体的な実装**: `JournalRepository` インターフェースで定義されたメソッドの具体的な処理を記述します。
*   **ファイル操作**: ファイルの読み書き、データのシリアライズ（Pythonのオブジェクトをファイルに保存できる形式に変換すること）とデシリアライズ（ファイルから読み込んだデータをPythonのオブジェクトに戻すこと）を行います。

**具体的な内容**
ここでは、データをJSON形式のファイルとして保存・読み込みする例を挙げます。JSONは人間にも読みやすく、プログラムでも扱いやすい形式です。

```python
# src/data/file_storage.py に書く内容のイメージ
import json
from typing import List
from src.core.models import Task, Event, Note # データモデルをインポート
from src.data.repository import JournalRepository # 定義したインターフェースをインポート

class JsonJournalRepository(JournalRepository): # JournalRepositoryインターフェースを実装する
    def __init__(self, file_path="journal_data.json"):
        self.file_path = file_path
        self._data = self._load_all_data() # アプリ起動時にデータを読み込む

    def _load_all_data(self):
        """ファイルから全てのデータを読み込む内部メソッド"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # JSONから読み込んだ辞書をPythonオブジェクトに変換する処理が必要
                # 例: data['tasks'] = [Task(**t) for t in data.get('tasks', [])]
                return data
        except FileNotFoundError: # ファイルがまだ存在しない場合
            return {"tasks": [], "events": [], "notes": []} # 空のデータを返す
        except json.JSONDecodeError: # ファイルの内容が不正なJSONの場合
            print(f"Warning: Corrupted data file at {self.file_path}. Starting with empty data.")
            return {"tasks": [], "events": [], "notes": []}

    def _save_all_data(self):
        """全てのデータをファイルに保存する内部メソッド"""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            # PythonオブジェクトをJSONに変換する処理が必要
            # 例: json.dump({"tasks": [t.__dict__ for t in self._data['tasks']]}, f, indent=4)
            json.dump(self._data, f, indent=4, ensure_ascii=False) # ensure_ascii=False で日本語もそのまま保存

    def save_tasks(self, tasks: List[Task]):
        """タスクのリストを保存する"""
        # Taskオブジェクトのリストを、JSONに変換しやすい辞書のリストに変換
        self._data['tasks'] = [t.__dict__ for t in tasks]
        self._save_all_data()

    def load_tasks(self) -> List[Task]:
        """タスクのリストを読み込む"""
        # 辞書のリストをTaskオブジェクトのリストに変換
        return [Task(**t) for t in self._data.get('tasks', [])]

    # イベントやメモについても同様に save_events, load_events などが実装されます
    # ...
```

---

このように、それぞれのファイルが明確な役割を持ち、連携することで、データの保存・読み込みという機能が実現されます。
