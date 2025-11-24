"""
四角形と透明度の例

半透明の四角形を重ねて描画し、アルファブレンディングの効果を示すサンプルです。
"""

import cv2

from blend2d import CompOp, Context, Image


def main():
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

    # 半透明の緑の四角形も追加
    ctx.set_fill_style_rgba(0, 255, 0, 128)  # 緑、50% 透明
    ctx.fill_rect(100, 180, 200, 150)

    ctx.end()

    # NumPy 配列として取得
    rgba = img.asarray()

    # OpenCV で表示（BGRA → BGR 変換）
    bgr = cv2.cvtColor(rgba, cv2.COLOR_BGRA2BGR)
    cv2.imshow("Rectangles with Transparency", bgr)

    print("Ctrl-C で終了します...")
    print("半透明の四角形が重なっている部分の色の混合を確認できます")

    try:
        while True:
            cv2.waitKey(1)
    except KeyboardInterrupt:
        print("\n終了します...")
    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
