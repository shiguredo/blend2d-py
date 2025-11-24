# example の実行方法

このディレクトリには blend2d‑py のサンプルが含まれます。OpenCV で描画結果を表示します。

## 事前準備

リポジトリ直下で次を実行します。

```bash
uv sync
```

備考: OpenCV 4.12 は NumPy < 2.3 を要求します。本プロジェクトの依存はそれに合わせて固定しています。

## 実行方法

以下はすべてリポジトリ直下で実行します。

- 基本の円: `uv run python examples/basic_circle.py`
- 透明な四角形: `uv run python examples/rectangles_transparency.py`
- パスの描画: `uv run python examples/path_drawing.py`
- 複数図形の組み合わせ: `uv run python examples/combined_shapes.py`
- アニメーション: `uv run python examples/animated_rectangles.py`
- リアルタイム描画デモ: `uv run python examples/realtime_demo.py`

ヒント: OpenCV のウィンドウは `Ctrl-C` で終了できます。

## 表示に関する注意

- 画像の内部形式は PRGB32（実質 BGRA）です。OpenCV で表示する際は `cv2.cvtColor(..., cv2.COLOR_BGRA2BGR)` により BGR に変換します。
- GUI 非対応環境ではウィンドウ表示ができません。
