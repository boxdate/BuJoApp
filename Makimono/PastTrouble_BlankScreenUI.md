# UI表示問題：アプリケーション起動時に白紙画面が表示される

## 1. 発生日時

2025年9月23日火曜日

## 2. 現象

アプリケーションを起動すると、タイトルバーは表示されるものの、アプリケーションウィンドウ内は白紙のままで、UIコンポーネントが一切表示されない状態となった。

## 3. 原因

`src/ui/main_window.py` 内の `MainWindow` クラスの `__init__` メソッドにおいて、メインレイアウト (`main_layout`) に主要なUIコンポーネント（`self.left_page`, `self.separator_line`, `self.right_page`）を追加するコードが、誤って `__init__` メソッドの *外* に移動し、`_move_focus_to_next_task` メソッドの *中* に配置されていたことが原因。

これにより、アプリケーションの初期化時にこれらのUIコンポーネントがメインレイアウトに正しく追加されず、結果として空のウィンドウが表示された。

## 4. デバッグプロセス

1.  **問題の切り分け**: アプリケーションがクラッシュしているのか、それともUIが単に表示されていないだけなのかを判断するため、`MainWindow.__init__` メソッドの様々な箇所に `print` 文を段階的に追加し、実行フローを確認した。
2.  **実行フローの追跡**: `print` 文の出力から、`MainWindow.__init__` メソッドの終盤、特に `main_layout.addWidget()` を呼び出すべき箇所で、それ以降の `print` 文が出力されていないことが判明した。
3.  **原因の特定**: 問題の箇所周辺のコードを詳細に確認した結果、`_move_focus_to_next_task` メソッドを挿入した際に、`main_layout.addWidget()` を含むコードブロックが誤って `__init__` メソッドのスコープ外に移動してしまっていたことを発見した。

## 5. 解決策

誤って移動していた以下のコードブロックを、`MainWindow.__init__` メソッド内の正しい位置（すべてのページコンポーネントが初期化された後、かつ `__init__` メソッドの終了前）に戻した。

```python
        main_layout.addWidget(self.left_page)

        # Add a vertical separator line
        self.separator_line = QFrame()
        self.separator_line.setFrameShape(QFrame.Shape.VLine)
        self.separator_line.setFrameShadow(QFrame.Shadow.Sunken)
        self.separator_line.setLineWidth(2) # Adjust thickness as needed
        main_layout.addWidget(self.separator_line)

        main_layout.addWidget(self.right_page)
```

## 6. 学習ポイント

*   **GUIアプリケーションの初期化**: `__init__` メソッドは、GUIアプリケーションのウィンドウやウィジェットの初期コンテンツとレイアウトを設定するために不可欠である。主要なUIコンポーネントがこの段階でレイアウトに追加されないと、画面に表示されない。
*   **コードの構造とスコープ**: コードブロックを移動したり、自動化されたツール（`replace` など）を使用したりする際には、コードの構造とスコープ（どのメソッドやクラスに属するか）に細心の注意を払う必要がある。わずかな配置ミスが、予期せぬ動作やバグにつながる。
*   **段階的なデバッグの有効性**: `print` 文を戦略的に配置し、実行フローを段階的に追跡するデバッグ手法は、特にGUIアプリケーションのようにエラーメッセージが直接表示されにくい場合でも、問題の発生箇所を特定するのに非常に有効である。
*   **「白紙画面」の症状**: GUIアプリケーションで白紙画面が表示される場合、多くはアプリケーションがクラッシュしているか、または表示されるべきウィジェットがメインレイアウトに正しく追加されていないかのいずれかである。