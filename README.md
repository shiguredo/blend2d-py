# blend2d-py

[![PyPI](https://img.shields.io/pypi/v/blend2d-py)](https://pypi.org/project/blend2d-py/)
[![SPEC 0 — Minimum Supported Dependencies](https://img.shields.io/badge/SPEC-0-green?labelColor=%23004811&color=%235CA038)](https://scientific-python.org/specs/spec-0000/)
[![image](https://img.shields.io/pypi/pyversions/blend2d-py.svg)](https://pypi.python.org/pypi/blend2d-py)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Actions status](https://github.com/shiguredo/blend2d-py/workflows/wheel/badge.svg)](https://github.com/shiguredo/blend2d-py/actions)

## About Shiguredo's open source software

We will not respond to PRs or issues that have not been discussed on Discord. Also, Discord is only available in Japanese.

Please read <https://github.com/shiguredo/oss/blob/master/README.en.md> before use.

## 時雨堂のオープンソースソフトウェアについて

利用前に <https://github.com/shiguredo/oss> をお読みください。

## blend2d-py について

高性能 2D ベクターグラフィックエンジン [Blend2D](https://blend2d.com/) の Python バインディングです。

<https://github.com/user-attachments/assets/b0edb8e0-c426-4523-ac87-e66c9aa04e61>

blend2d-py と [raw-player](https://github.com/shiguredo/raw-player) を組み合わせて 120 fps での映像なども描画可能です。

## 特徴

- [numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html) によるピクセルデータの受け渡し
- ピクセルデータへの直接アクセス (`Image.asarray()` / `Image.memoryview()`)
- 基本図形の描画 (四角形、円、扇形)
- ベクターパスによる自由な図形描画 (直線、ベジェ曲線、円弧)
- 線形/放射状/円錐グラデーション
- パターン塗りつぶし
- ストローク描画 (線幅、キャップ、ジョイン)
- アルファブレンディング
- 座標変換 (平行移動、回転)
- マルチスレッドレンダリング
- テキスト描画 (macOS のみ)
- Python [Free-Threading](https://docs.python.org/3/howto/free-threading-python.html)

## 対応プラットフォーム

- macOS 26 arm64
- macOS 15 arm64
- Ubuntu 24.04 x86_64
- Ubuntu 24.04 arm64
- Ubuntu 22.04 x86_64
- Ubuntu 22.04 arm64
- Windows Server 2025 x86_64
- Windows 11 x86_64

## 対応 Python

- 3.14
- 3.14t
- 3.13
- 3.13t
- 3.12

## インストール

```bash
uv add blend2d-py
```

## 使い方

### 基本的な円の描画

```python
from math import pi
from blend2d import Image, Context, CompOp

# 画像サイズを指定
w, h = 640, 360
img = Image(w, h)

with Context(img) as ctx:
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

    # NumPy 配列として取得
    rgba = img.asarray()  # (H, W, 4) uint8 (BGRA)
```

### 四角形と透明度の例

```python
from blend2d import Image, Context, CompOp

w, h = 640, 480
img = Image(w, h)

with Context(img) as ctx:
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
```

### パスを使った図形描画

```python
from blend2d import Image, Context, Path, CompOp

w, h = 640, 480
img = Image(w, h)

# パスで三角形を作成
path = Path()
path.move_to(w/2, h/4)      # 頂点
path.line_to(w/4, 3*h/4)    # 左下
path.line_to(3*w/4, 3*h/4)  # 右下
path.close()                # パスを閉じる

with Context(img) as ctx:
    # 背景を暗い灰色に
    ctx.set_fill_style_rgba(40, 40, 40, 255)
    ctx.fill_all()

    # グラデーション風に複数の色で描画
    colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255)]
    for i, color in enumerate(colors):
        ctx.save()  # 現在の状態を保存
        ctx.translate(i * 10, i * 10)  # 少しずつずらす
        ctx.set_fill_style_rgba(*color, 200 - i * 50)  # 透明度を変える
        ctx.fill_path(path)
        ctx.restore()  # 状態を復元
```

### 複数の図形を組み合わせる例

```python
import colorsys
from math import pi, sin, cos
from blend2d import Image, Context

w, h = 640, 480
img = Image(w, h)

with Context(img) as ctx:
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
        r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        ctx.set_fill_style_rgba(int(r * 255), int(g * 255), int(b * 255), 200)
        ctx.fill_circle(x, y, 20)  # 小さな円を描画
```

### テキスト描画 (macOS のみ)

```python
from blend2d import Image, Context, Font, FontFace

w, h = 640, 480
img = Image(w, h)

# フォントをロード (macOS のシステムフォント)
face = FontFace()
face.create_from_file("/System/Library/Fonts/Helvetica.ttc")

# フォントインスタンスを作成
font = Font(face, 48.0)

with Context(img) as ctx:
    # 背景を白で塗りつぶし
    ctx.set_fill_style_rgba(255, 255, 255, 255)
    ctx.fill_all()

    # テキストを描画
    ctx.set_fill_style_rgba(0, 0, 0, 255)
    ctx.fill_utf8_text(50, 100, font, "Hello, Blend2D!")
```

> [!NOTE]
>
> - テキスト描画機能は macOS のシステムフォントを使用するため、macOS でのみ動作します
> - `asarray()` / `memoryview()` のビューは `Image` の寿命に依存します

## API リファレンス

### Image

描画対象となる画像バッファを管理するクラス。

```python
img = Image(width, height)
```

| メソッド | 説明 |
|----------|------|
| `asarray()` | NumPy 配列として取得 (H, W, 4) uint8 BGRA |
| `memoryview()` | PEP 3118 memoryview を取得 (1D, size=stride*height) |

| プロパティ | 説明 |
|------------|------|
| `width` | 画像の幅 |
| `height` | 画像の高さ |

### Context

描画コンテキストを管理するクラス。with 文で使用可能。

```python
with Context(img, thread_count=0) as ctx:
    ctx.fill_all()
```

#### コンテキスト管理

| メソッド | 説明 |
|----------|------|
| `end()` | コンテキストを終了 |
| `save()` | 現在の状態をスタックに保存 |
| `restore()` | 保存した状態を復元 |

#### 塗りつぶしスタイル

| メソッド | 説明 |
|----------|------|
| `set_comp_op(op)` | 合成モードを設定 |
| `set_fill_style_rgba(r, g, b, a=255)` | 塗りつぶし色を RGBA で設定 |
| `set_fill_style_gradient(gradient)` | 塗りつぶしをグラデーションに設定 |
| `set_fill_style_pattern(pattern)` | 塗りつぶしをパターンに設定 |

#### ストロークスタイル

| メソッド | 説明 |
|----------|------|
| `set_stroke_style_rgba(r, g, b, a=255)` | ストローク色を RGBA で設定 |
| `set_stroke_style_gradient(gradient)` | ストロークをグラデーションに設定 |
| `set_stroke_style_pattern(pattern)` | ストロークをパターンに設定 |
| `set_stroke_width(width)` | ストローク幅を設定 |
| `set_stroke_miter_limit(miter_limit)` | マイターリミットを設定 |
| `set_stroke_join(stroke_join)` | ジョインスタイルを設定 |
| `set_stroke_caps(stroke_cap)` | キャップスタイルを設定 |

#### 座標変換

| メソッド | 説明 |
|----------|------|
| `translate(x, y)` | 座標系を平行移動 |
| `rotate(rad)` | 座標系を回転 (ラジアン) |

#### 塗りつぶし描画

| メソッド | 説明 |
|----------|------|
| `fill_all()` | 全体を塗りつぶし |
| `fill_rect(x, y, w, h)` | 四角形を塗りつぶし |
| `fill_circle(cx, cy, r)` | 円を塗りつぶし |
| `fill_pie(cx, cy, r, start, sweep)` | 扇形を塗りつぶし |
| `fill_path(path)` | パスを塗りつぶし |
| `fill_utf8_text(x, y, font, text)` | テキストを描画 (macOS のみ) |

#### ストローク描画

| メソッド | 説明 |
|----------|------|
| `stroke_rect(x, y, w, h)` | 四角形のストローク |
| `stroke_circle(cx, cy, r)` | 円のストローク |
| `stroke_path(path)` | パスのストローク |

### Path

ベクターパスを作成するクラス。

```python
path = Path()
path.move_to(x, y)
path.line_to(x, y)
path.close()
```

| メソッド | 説明 |
|----------|------|
| `move_to(x, y)` | 指定座標に移動 |
| `line_to(x, y)` | 直線を描画 |
| `quad_to(x1, y1, x2, y2)` | 二次ベジェ曲線を描画 |
| `cubic_to(x1, y1, x2, y2, x3, y3)` | 三次ベジェ曲線を描画 |
| `smooth_quad_to(x2, y2)` | スムーズな二次ベジェ曲線 |
| `smooth_cubic_to(x2, y2, x3, y3)` | スムーズな三次ベジェ曲線 |
| `arc_to(cx, cy, rx, ry, start, sweep, force_move_to=False)` | 円弧を描画 |
| `elliptic_arc_to(rx, ry, x_axis_rotation, large_arc_flag, sweep_flag, x, y)` | 楕円弧を描画 (SVG 互換) |
| `close()` | パスを閉じる |

### Gradient

グラデーションを定義するクラス。

```python
gradient = Gradient()
gradient.create_linear(x0, y0, x1, y1)
gradient.add_stop(0.0, 255, 0, 0)    # 赤
gradient.add_stop(1.0, 0, 0, 255)    # 青
```

| メソッド | 説明 |
|----------|------|
| `create_linear(x0, y0, x1, y1, extend_mode=PAD)` | 線形グラデーションを作成 |
| `create_radial(x0, y0, x1, y1, r0, extend_mode=PAD, r1=0.0)` | 放射状グラデーションを作成 |
| `create_conic(x0, y0, angle, extend_mode=PAD, repeat=1.0)` | 円錐グラデーションを作成 |
| `add_stop(offset, r, g, b, a=255)` | カラーストップを追加 (offset: 0.0〜1.0) |
| `reset_stops()` | 全てのカラーストップをリセット |

| プロパティ | 説明 |
|------------|------|
| `stop_count` | カラーストップの数 |
| `gradient_type` | グラデーションの種類 (LINEAR / RADIAL / CONIC) |
| `extend_mode` | 拡張モード |

### Pattern

パターン塗りつぶしを定義するクラス。

```python
pattern = Pattern()
pattern.create(image, extend_mode=REPEAT)
```

| メソッド | 説明 |
|----------|------|
| `create(image, extend_mode=REPEAT)` | パターンを作成 |
| `set_area(x, y, w, h)` | パターン領域を設定 |
| `reset_area()` | パターン領域をリセット |
| `set_extend_mode(extend_mode)` | 拡張モードを設定 |

| プロパティ | 説明 |
|------------|------|
| `extend_mode` | 拡張モード |

### FontFace

フォントフェイスを管理するクラス。

```python
face = FontFace()
face.create_from_file("/System/Library/Fonts/Helvetica.ttc")
```

| メソッド | 説明 |
|----------|------|
| `create_from_file(filename)` | ファイルからフォントを読み込み |

| プロパティ | 説明 |
|------------|------|
| `family_name` | フォントファミリー名 |
| `weight` | フォントウェイト |

### Font

フォントインスタンスを管理するクラス。

```python
font = Font(face, size=48.0)
```

| プロパティ | 説明 |
|------------|------|
| `size` | フォントサイズ |

### 列挙型

#### CompOp (合成モード)

| 値 | 説明 |
|----|------|
| `SRC_COPY` | ソースをそのままコピー (不透明描画) |
| `SRC_OVER` | ソースを上に重ねる (アルファブレンディング) |

#### ExtendMode (拡張モード)

| 値 | 説明 |
|----|------|
| `PAD` | 端のピクセルで拡張 |
| `REPEAT` | 繰り返し |
| `REFLECT` | 反射 (ミラー) |

#### GradientType (グラデーション種類)

| 値 | 説明 |
|----|------|
| `LINEAR` | 線形グラデーション |
| `RADIAL` | 放射状グラデーション |
| `CONIC` | 円錐グラデーション |

#### StrokeCap (ストロークキャップ)

| 値 | 説明 |
|----|------|
| `BUTT` | 端で切断 |
| `SQUARE` | 四角形で延長 |
| `ROUND` | 丸く延長 |
| `ROUND_REV` | 内側に丸く |
| `TRIANGLE` | 三角形で延長 |
| `TRIANGLE_REV` | 内側に三角形 |

#### StrokeJoin (ストロークジョイン)

| 値 | 説明 |
|----|------|
| `MITER_CLIP` | マイター結合 (クリップ) |
| `MITER_BEVEL` | マイター結合 (ベベル) |
| `MITER_ROUND` | マイター結合 (丸) |
| `BEVEL` | ベベル結合 |
| `ROUND` | 丸結合 |

## ビルド

```bash
uv build --wheel
```

## サンプル

```bash
uv sync --group example
uv build --wheel
uv pip install -e . --force-reinstall
uv run python examples/realtime_demo.py
```

- PRGB32（実質 BGRA）→ `cv2.cvtColor(..., cv2.COLOR_BGRA2BGR)` で表示
- 詳細手順と他のサンプルは `examples/README.md` を参照

## Blend2D ライセンス

zlib License

```text
Copyright (c) 2017-2025 Petr Kobalicek, Fabian Yzerman

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
