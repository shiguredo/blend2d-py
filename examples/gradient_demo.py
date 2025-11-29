#!/usr/bin/env python3
"""グラデーション描画のデモ"""

import blend2d

# 画像の作成
img = blend2d.Image(640, 480)

with blend2d.Context(img) as ctx:
    # 背景を白で塗りつぶし
    ctx.set_fill_style_rgba(255, 255, 255)
    ctx.fill_all()

    # Linear Gradient (線形グラデーション)
    linear_grad = blend2d.Gradient()
    linear_grad.create_linear(50.0, 50.0, 250.0, 50.0)
    linear_grad.add_stop(0.0, 255, 0, 0)  # 赤
    linear_grad.add_stop(0.5, 0, 255, 0)  # 緑
    linear_grad.add_stop(1.0, 0, 0, 255)  # 青

    ctx.set_fill_style_gradient(linear_grad)
    ctx.fill_rect(50.0, 50.0, 200.0, 100.0)

    # Radial Gradient (放射状グラデーション)
    radial_grad = blend2d.Gradient()
    radial_grad.create_radial(450.0, 100.0, 450.0, 100.0, 80.0)
    radial_grad.add_stop(0.0, 255, 255, 0)  # 黄色
    radial_grad.add_stop(1.0, 255, 0, 255)  # マゼンタ

    ctx.set_fill_style_gradient(radial_grad)
    ctx.fill_circle(450.0, 100.0, 80.0)

    # Conic Gradient (円錐形グラデーション)
    conic_grad = blend2d.Gradient()
    conic_grad.create_conic(320.0, 350.0, 0.0)
    conic_grad.add_stop(0.0, 255, 0, 0)  # 赤
    conic_grad.add_stop(0.33, 0, 255, 0)  # 緑
    conic_grad.add_stop(0.66, 0, 0, 255)  # 青
    conic_grad.add_stop(1.0, 255, 0, 0)  # 赤

    ctx.set_fill_style_gradient(conic_grad)
    ctx.fill_circle(320.0, 350.0, 80.0)

# NumPy 配列として取得
arr = img.asarray()
print(f"Image shape: {arr.shape}, dtype: {arr.dtype}")

# 画像を保存 (cv2 を使う場合)
try:
    import cv2

    # BGRA -> BGR 変換 (アルファチャンネル除去)
    bgr = arr[:, :, :3]
    cv2.imwrite("gradient_demo.png", bgr)
    print("Saved: gradient_demo.png")
except ImportError:
    print("opencv-python がインストールされていません")
    print("画像を保存するには: uv pip install opencv-python")
