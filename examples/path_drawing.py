"""
パスを使った図形描画

Path を使って三角形を作成し、グラデーション風の効果を加えるサンプルです。
"""

import cv2

from blend2d import Context, Image, Path


def main():
    w, h = 640, 480
    img = Image(w, h)
    ctx = Context(img)

    # 背景を暗い灰色に
    ctx.set_fill_style_rgba(40, 40, 40, 255)
    ctx.fill_all()

    # パスで三角形を作成
    path = Path()
    path.move_to(w / 2, h / 4)  # 頂点
    path.line_to(w / 4, 3 * h / 4)  # 左下
    path.line_to(3 * w / 4, 3 * h / 4)  # 右下
    path.close()  # パスを閉じる

    # グラデーション風に複数の色で描画
    colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255)]
    for i, color in enumerate(colors):
        ctx.save()  # 現在の状態を保存
        ctx.translate(i * 10, i * 10)  # 少しずつずらす
        ctx.set_fill_style_rgba(*color, 200 - i * 50)  # 透明度を変える
        ctx.fill_path(path)
        ctx.restore()  # 状態を復元

    # 星形のパスも追加で描画
    import math

    star_path = Path()
    cx, cy = w * 0.8, h * 0.3  # 星の中心
    radius_outer = 50
    radius_inner = 20

    for i in range(10):
        angle = i * math.pi / 5
        if i % 2 == 0:
            x = cx + radius_outer * math.cos(angle)
            y = cy + radius_outer * math.sin(angle)
        else:
            x = cx + radius_inner * math.cos(angle)
            y = cy + radius_inner * math.sin(angle)

        if i == 0:
            star_path.move_to(x, y)
        else:
            star_path.line_to(x, y)

    star_path.close()

    # 星を黄色で描画
    ctx.set_fill_style_rgba(255, 255, 0, 255)
    ctx.fill_path(star_path)

    ctx.end()

    # NumPy 配列として取得
    rgba = img.asarray()

    # OpenCV で表示（BGRA → BGR 変換）
    bgr = cv2.cvtColor(rgba, cv2.COLOR_BGRA2BGR)
    cv2.imshow("Path Drawing", bgr)

    print("Ctrl-C で終了します...")
    print("パスを使って三角形と星形を描画しています")

    try:
        while True:
            cv2.waitKey(1)
    except KeyboardInterrupt:
        print("\n終了します...")
    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
