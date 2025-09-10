# PEP 3118 バッファ対応（memoryview / NumPy 連携）

本パッケージの `Image` は内部ピクセル（PRGB32: 8 bit BGRA）を PEP 3118 準拠のバッファとして公開します。ゼロコピーで取得でき、書き込みは元画像へ反映されます。

## 前提・要件

- **NumPy**: `asarray()` 利用時に必須（2.x）。OpenCV 4.12 と併用する場合は互換性のため NumPy は 2.3 未満を推奨。

## 提供 API

- `Image.memoryview() -> memoryview`
  - 先頭から `stride * height` バイトの 1 次元ビューを返します（ゼロコピー、書き込み可）。
  - 形状は 1 次元ですが、NumPy や `memoryview.cast` で再解釈できます。
- `Image.asarray() -> numpy.ndarray`
  - `(H, W, 4)` の `uint8` ビューをゼロコピーで返します（書き込み可）。
  - 実装は `memoryview` を介した `numpy.frombuffer` によるビューでコピーは発生しません。

## データ仕様

- **フォーマット**: PRGB32（プリマルチプライド BGRA）
- **行ピッチ**: 各行のバイト数は `stride` で、`W * 4` 以上になる場合があります。
- **連続性**: 行ピッチのため、`rgba.flags["C_CONTIGUOUS"]` は `False` になることがあります。連続メモリが必要なら `np.ascontiguousarray(rgba)` で明示的にコピーしてください。

## NumPy のゼロコピー ndarray に変換

```python
import numpy as np

h, w = img.height, img.width
mv = img.memoryview()                         # 1 次元: stride * h bytes
row_bytes = np.frombuffer(mv, np.uint8).reshape(h, -1)
rgba = row_bytes[:, : w * 4].reshape(h, w, 4)  # (H, W, 4) BGRA

# もしくは簡単に
rgba2 = img.asarray()
```

`row_bytes` は行ピッチ（stride）を保持した 2 次元の `uint8` 配列です。必要な幅 `w * 4` のみをスライスし、`(H, W, 4)` の BGRA 表現へ再解釈します。

## OpenCV で表示

```python
import cv2

bgr = cv2.cvtColor(rgba, cv2.COLOR_BGRA2BGR)
cv2.imshow("win", bgr)
cv2.waitKey(1)
```

## 注意事項 / 補足

- **寿命**: ビュー（`memoryview` / `ndarray`）は `Image` の寿命に依存します。`Image` より長生きさせないでください。
- **書き込み**: ビューへの書き込みは元のピクセルに反映されます。
- **cast の制限**: `memoryview.cast()` は非連続メモリ（行ピッチあり）の多次元化に制限があります。確実性重視なら上記の NumPy 変換を使ってください。
