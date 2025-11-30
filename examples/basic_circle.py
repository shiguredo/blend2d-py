"""
基本的な円の描画サンプル

Blend2D で基本的な円を描画し、OpenCV で表示するサンプルです。
"""

from math import pi

import cv2

from blend2d import CompOp, Context, Image


def main():
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
        ctx.translate(w * 0.5, h * 0.5)

        # 白い円を描画
        ctx.set_fill_style_rgba(255, 255, 255, 255)
        ctx.fill_pie(0, 0, min(w, h) * 0.3, 0, 2 * pi)

    # NumPy 配列として取得（ゼロコピー）
    rgba = img.asarray()  # (H, W, 4) uint8 (BGRA)

    # OpenCV で表示（BGRA → BGR 変換）
    bgr = cv2.cvtColor(rgba, cv2.COLOR_BGRA2BGR)
    cv2.imshow("Basic Circle", bgr)

    print("Ctrl-C で終了します...")
    try:
        while True:
            cv2.waitKey(1)
    except KeyboardInterrupt:
        print("\n終了します...")
    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
