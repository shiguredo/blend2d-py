# blend2d-py

[![PyPI](https://img.shields.io/pypi/v/blend2d-py)](https://pypi.org/project/blend2d-py/)
[![image](https://img.shields.io/pypi/pyversions/blend2d-py.svg)](https://pypi.python.org/pypi/blend2d-py)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Actions status](https://github.com/shiguredo/blend2d-py/workflows/build/badge.svg)](https://github.com/shiguredo/blend2d-py/actions)

## About Shiguredo's open source software

We will not respond to PRs or issues that have not been discussed on Discord. Also, Discord is only available in Japanese.

Please read <https://github.com/shiguredo/oss/blob/master/README.en.md> before use.

## 時雨堂のオープンソースソフトウェアについて

利用前に <https://github.com/shiguredo/oss> をお読みください。

## blend2d-py について

高性能 2D ベクターグラフィックエンジン [blend2d](https://blend2d.com/) の Python バインディングです。

## 対応プラットフォーム

- macOS 15 arm64
- macOS 14 arm64
- Ubuntu 24.04 x86_64
- Ubuntu 24.04 arm64

## 対応 Python

- 3.13
- 3.12
- 3.11

## インストール

```bash
uv add blend2d-py
```

## 使い方（最小 API）

- 提供: `Image`, `Context`, `Path`, `CompOp`
- ピクセルアクセス: `Image.asarray()` / `Image.memoryview()`（ゼロコピー）

### 基本的な円の描画

```python
from math import pi
from blend2d import Image, Context, CompOp

# 画像サイズを指定
w, h = 640, 360
img = Image(w, h)
ctx = Context(img)

# 合成モードを設定（SRC_COPY は不透明描画）
ctx.set_comp_op(CompOp.SRC_COPY)

# 背景を黒で塗りつぶし
ctx.set_fill_style_rgba(0, 0, 0, 255)
ctx.fill_all()

# 中心に移動
ctx.translate(w*0.5, h*0.5)

# 白い円を描画
ctx.set_fill_style_rgba(255, 255, 255, 255)
ctx.fill_pie(0, 0, min(w, h)*0.3, 0, 2*pi)

# NumPy 配列として取得（ゼロコピー）
rgba = img.asarray()  # (H, W, 4) uint8 (BGRA)
ctx.end()
```

### 四角形と透明度の例

```python
from blend2d import Image, Context, CompOp

w, h = 640, 480
img = Image(w, h)
ctx = Context(img)

# 背景を白で塗りつぶし
ctx.set_fill_style_rgba(255, 255, 255, 255)
ctx.fill_all()

# 半透明の赤い四角形を描画
ctx.set_comp_op(CompOp.SRC_OVER)  # アルファブレンディングを有効化
ctx.set_fill_style_rgba(255, 0, 0, 128)  # 赤、50% 透明
ctx.fill_rect(50, 50, 200, 150)

# 半透明の青い四角形を重ねて描画
ctx.set_fill_style_rgba(0, 0, 255, 128)  # 青、50% 透明
ctx.fill_rect(150, 100, 200, 150)

ctx.end()
```

### パスを使った図形描画

```python
from blend2d import Image, Context, Path, CompOp

w, h = 640, 480
img = Image(w, h)
ctx = Context(img)

# 背景を暗い灰色に
ctx.set_fill_style_rgba(40, 40, 40, 255)
ctx.fill_all()

# パスで三角形を作成
path = Path()
path.move_to(w/2, h/4)      # 頂点
path.line_to(w/4, 3*h/4)    # 左下
path.line_to(3*w/4, 3*h/4)  # 右下
path.close()                # パスを閉じる

# グラデーション風に複数の色で描画
colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255)]
for i, color in enumerate(colors):
    ctx.save()  # 現在の状態を保存
    ctx.translate(i * 10, i * 10)  # 少しずつずらす
    ctx.set_fill_style_rgba(*color, 200 - i * 50)  # 透明度を変える
    ctx.fill_path(path)
    ctx.restore()  # 状態を復元

ctx.end()
```

### 複数の図形を組み合わせる例

```python
from math import pi, sin, cos
from blend2d import Image, Context, CompOp

w, h = 640, 480
img = Image(w, h)
ctx = Context(img)

# 背景を黒に
ctx.set_fill_style_rgba(0, 0, 0, 255)
ctx.fill_all()

# 円を円形に配置
ctx.translate(w/2, h/2)  # 中心に移動
num_circles = 12
radius = 100

for i in range(num_circles):
    angle = 2 * pi * i / num_circles
    x = radius * cos(angle)
    y = radius * sin(angle)
    
    # 虹色のグラデーション
    hue = i / num_circles
    r = int(255 * (1 - hue) if hue < 0.5 else 0)
    g = int(255 * hue if hue < 0.5 else 255 * (1 - hue))
    b = int(0 if hue < 0.5 else 255 * hue)
    
    ctx.set_fill_style_rgba(r, g, b, 200)
    ctx.fill_circle(x, y, 20)  # 小さな円を描画

ctx.end()
```

> [!WARNING]
>
> - `asarray()` / `memoryview()` のビューは `Image` の寿命に依存します
> - フォント描画やエンコードは未ラップです

## サンプル

- 実行: `uv run python example/realtime_demo.py`
- PRGB32（実質 BGRA）→ `cv2.cvtColor(..., cv2.COLOR_BGRA2BGR)` で表示。
- 詳細手順と他のサンプルは `example/README.md` を参照。

## ビルド

```bash
uv build --wheel
```

## PEP 3118 バッファ

- `Image.memoryview()` で `stride*height` バイトの 1D バッファを公開します
- NumPy での多次元化や OpenCV 表示は `doc/buffer.md` を参照してください

## Blend2D ライセンス

zlib License

```text
Copyright (c) 2017-2024 The Blend2D Authors

This software is provided 'as-is', without any express or implied
warranty. In no event will the authors be held liable for any damages
arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to the following restrictions:

1. The origin of this software must not be misrepresented; you must not
   claim that you wrote the original software. If you use this software
   in a product, an acknowledgment in the product documentation would be
   appreciated but is not required.
2. Altered source versions must be plainly marked as such, and must not be
   misrepresented as being the original software.
3. This notice may not be removed or altered from any source distribution.
```

## blend2d-py ライセンス

Apache License 2.0

```text
Copyright 2025-2025, Shiguredo Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
