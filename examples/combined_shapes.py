"""
複数の図形を組み合わせる例

円を円形に配置して、虹色のグラデーションパターンを作成するサンプルです。
"""

from math import cos, pi, sin

import cv2

from blend2d import CompOp, Context, Image


def main():
    w, h = 640, 480
    img = Image(w, h)

    with Context(img) as ctx:
        # 背景を黒に
        ctx.set_fill_style_rgba(0, 0, 0, 255)
        ctx.fill_all()

        # 円を円形に配置
        ctx.translate(w / 2, h / 2)  # 中心に移動
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

        # 中心にも大きな円を追加
        ctx.set_comp_op(CompOp.SRC_OVER)
        ctx.set_fill_style_rgba(255, 255, 255, 100)  # 半透明の白
        ctx.fill_circle(0, 0, 50)

        # 外側にリングも追加
        ctx.set_fill_style_rgba(100, 100, 255, 150)  # 薄い青
        for i in range(24):
            angle = 2 * pi * i / 24
            x = radius * 2 * cos(angle)
            y = radius * 2 * sin(angle)
            ctx.fill_circle(x, y, 8)

    # NumPy 配列として取得
    rgba = img.asarray()

    # OpenCV で表示（BGRA → BGR 変換）
    bgr = cv2.cvtColor(rgba, cv2.COLOR_BGRA2BGR)
    cv2.imshow("Combined Shapes", bgr)

    print("Ctrl-C で終了します...")
    print("円形配置と虹色グラデーションのパターンを表示しています")

    try:
        while True:
            cv2.waitKey(1)
    except KeyboardInterrupt:
        print("\n終了します...")
    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
