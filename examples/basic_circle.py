"""
基本的な円の描画サンプル

Blend2D で基本的な円を描画し、raw-player で表示するサンプルです。
"""

from math import pi

from blend2d import CompOp, Context, Image
from raw_player import VideoPlayer


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
    bgra = img.asarray()  # (H, W, 4) uint8 (BGRA)

    # raw-player で表示
    player = VideoPlayer(width=w, height=h, title="Basic Circle")
    player.enqueue_video_bgra(bgra, 0)

    # キーコールバックを設定（ESC または q で終了）
    def on_key(key: int) -> bool:
        if key == 27 or key == 113:  # ESC or 'q'
            return False
        return True

    player.set_key_callback(on_key)
    player.play()

    print("ESC または q キーで終了します...")
    while player.is_open:
        if not player.poll_events():
            break

    player.close()
    print("終了します...")


if __name__ == "__main__":
    main()
