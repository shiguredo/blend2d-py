"""
四角形と透明度の例

半透明の四角形を重ねて描画し、アルファブレンディングの効果を示すサンプルです。
"""

from blend2d import CompOp, Context, Image
from raw_player import VideoPlayer


def main():
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

        # 半透明の緑の四角形も追加
        ctx.set_fill_style_rgba(0, 255, 0, 128)  # 緑、50% 透明
        ctx.fill_rect(100, 180, 200, 150)

    # NumPy 配列として取得
    bgra = img.asarray()

    # raw-player で表示
    player = VideoPlayer(width=w, height=h, title="Rectangles with Transparency")
    player.enqueue_video_bgra(bgra, 0)

    # キーコールバックを設定（ESC または q で終了）
    def on_key(key: int) -> bool:
        if key == 27 or key == 113:  # ESC or 'q'
            return False
        return True

    player.set_key_callback(on_key)
    player.play()

    print("ESC または q キーで終了します...")
    print("半透明の四角形が重なっている部分の色の混合を確認できます")

    while player.is_open:
        if not player.poll_events():
            break

    player.close()
    print("終了します...")


if __name__ == "__main__":
    main()
