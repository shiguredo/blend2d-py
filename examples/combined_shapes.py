"""
複数の図形を組み合わせる例

円を円形に配置して、虹色のグラデーションパターンを作成するサンプルです。
"""

import colorsys
from math import cos, pi, sin

from blend2d import CompOp, Context, Image
from raw_player import VideoPlayer


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
            r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
            ctx.set_fill_style_rgba(int(r * 255), int(g * 255), int(b * 255), 200)
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
    bgra = img.asarray()

    # raw-player で表示
    player = VideoPlayer(width=w, height=h, title="Combined Shapes")
    player.enqueue_video_bgra(bgra, 0)

    # キーコールバックを設定（ESC または q で終了）
    def on_key(key: int) -> bool:
        if key == 27 or key == 113:  # ESC or 'q'
            return False
        return True

    player.set_key_callback(on_key)
    player.play()

    print("ESC または q キーで終了します...")
    print("円形配置と虹色グラデーションのパターンを表示しています")

    while player.is_open:
        if not player.poll_events():
            break

    player.close()
    print("終了します...")


if __name__ == "__main__":
    main()
