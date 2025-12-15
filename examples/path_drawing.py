"""
パスを使った図形描画

Path を使って三角形を作成し、グラデーション風の効果を加えるサンプルです。
"""

import math

from blend2d import Context, Image, Path
from raw_player import VideoPlayer


def main():
    w, h = 640, 480
    img = Image(w, h)

    with Context(img) as ctx:
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

    # NumPy 配列として取得
    bgra = img.asarray()

    # raw-player で表示
    player = VideoPlayer(width=w, height=h, title="Path Drawing")
    player.enqueue_video_bgra(bgra, 0)

    # キーコールバックを設定（ESC または q で終了）
    def on_key(key: int) -> bool:
        if key == 27 or key == 113:  # ESC or 'q'
            return False
        return True

    player.set_key_callback(on_key)
    player.play()

    print("ESC または q キーで終了します...")
    print("パスを使って三角形と星形を描画しています")

    while player.is_open:
        if not player.poll_events():
            break

    player.close()
    print("終了します...")


if __name__ == "__main__":
    main()
