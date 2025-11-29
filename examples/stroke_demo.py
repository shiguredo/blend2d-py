#!/usr/bin/env python3
"""
Stroke デモ

線描画 (stroke) のサンプルです。
"""

import math

import cv2

from blend2d import CompOp, Context, Gradient, Image, Path


def main():
    w, h = 800, 600

    img = Image(w, h)

    with Context(img) as ctx:
        # 背景を白で塗りつぶし
        ctx.set_fill_style_rgba(255, 255, 255, 255)
        ctx.fill_all()

        ctx.set_comp_op(CompOp.SRC_OVER)

        # 1. 基本的な矩形の stroke (赤)
        ctx.set_stroke_style_rgba(255, 0, 0, 255)
        ctx.set_stroke_width(3.0)
        ctx.stroke_rect(50.0, 50.0, 200.0, 150.0)

        # 2. 太い線幅の矩形 (青)
        ctx.set_stroke_style_rgba(0, 0, 255, 255)
        ctx.set_stroke_width(10.0)
        ctx.stroke_rect(300.0, 50.0, 200.0, 150.0)

        # 3. 円の stroke (緑)
        ctx.set_stroke_style_rgba(0, 255, 0, 255)
        ctx.set_stroke_width(5.0)
        ctx.stroke_circle(150.0, 400.0, 80.0)

        # 4. グラデーションで stroke (線形グラデーション)
        grad = Gradient()
        grad.create_linear(350.0, 250.0, 550.0, 250.0)
        grad.add_stop(0.0, 255, 0, 0, 255)  # 赤
        grad.add_stop(0.5, 0, 255, 0, 255)  # 緑
        grad.add_stop(1.0, 0, 0, 255, 255)  # 青

        ctx.set_stroke_style_gradient(grad)
        ctx.set_stroke_width(8.0)
        ctx.stroke_circle(450.0, 400.0, 80.0)

        # 5. Path の stroke (星型)
        path = Path()
        cx, cy = 650.0, 350.0
        r_outer, r_inner = 80.0, 35.0
        points = 5

        for i in range(points * 2):
            angle = math.pi * 2 * i / (points * 2) - math.pi / 2
            r = r_outer if i % 2 == 0 else r_inner
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)

            if i == 0:
                path.move_to(x, y)
            else:
                path.line_to(x, y)
        path.close()

        ctx.set_stroke_style_rgba(255, 165, 0, 255)  # オレンジ
        ctx.set_stroke_width(4.0)
        ctx.stroke_path(path)

    # NumPy 配列として取得
    rgba = img.asarray()

    # OpenCV で表示（BGRA → BGR 変換）
    bgr = cv2.cvtColor(rgba, cv2.COLOR_BGRA2BGR)
    cv2.imshow("Stroke Demo", bgr)

    print("Stroke デモ")
    print("1. 左上: 基本的な矩形 stroke (赤, 線幅 3)")
    print("2. 右上: 太い線幅の矩形 (青, 線幅 10)")
    print("3. 左下: 円の stroke (緑, 線幅 5)")
    print("4. 中央下: グラデーション stroke (線幅 8)")
    print("5. 右中央: Path の stroke - 星型 (オレンジ, 線幅 4)")
    print("")
    print("何かキーを押すと終了します...")

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
