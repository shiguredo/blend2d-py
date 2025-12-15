"""
テキスト描画サンプル (macOS のみ)

Blend2D でテキストを描画し、raw-player で表示するサンプルです。
macOS のシステムフォントを使用するため、macOS でのみ動作します。
"""

from blend2d import CompOp, Context, Font, FontFace, Image
from raw_player import VideoPlayer


def main():
    # 画像サイズを指定
    w, h = 640, 480
    img = Image(w, h)

    with Context(img) as ctx:
        # 合成モードを設定（SRC_COPY は不透明描画）
        ctx.set_comp_op(CompOp.SRC_COPY)

        # 背景を白で塗りつぶし
        ctx.set_fill_style_rgba(255, 255, 255, 255)
        ctx.fill_all()

        # フォントをロード (macOS のシステムフォント)
        face = FontFace()
        face.create_from_file("/System/Library/Fonts/Helvetica.ttc")

        # 大きいフォントを作成
        large_font = Font(face, 48.0)

        # テキストを描画（黒）
        ctx.set_fill_style_rgba(0, 0, 0, 255)
        ctx.fill_utf8_text(50, 100, large_font, "Hello, Blend2D!")

        # 中サイズのフォントを作成
        medium_font = Font(face, 32.0)

        # 別のテキストを描画（青）
        ctx.set_fill_style_rgba(0, 64, 192, 255)
        ctx.fill_utf8_text(50, 180, medium_font, "Text Rendering Sample")

        # 小さいフォントを作成
        small_font = Font(face, 24.0)

        # 情報を描画（灰色）
        ctx.set_fill_style_rgba(128, 128, 128, 255)
        ctx.fill_utf8_text(50, 250, small_font, f"Font: {face.family_name} (Weight: {face.weight})")
        ctx.fill_utf8_text(50, 290, small_font, f"Large: {large_font.size}px")
        ctx.fill_utf8_text(50, 330, small_font, f"Medium: {medium_font.size}px")
        ctx.fill_utf8_text(50, 370, small_font, f"Small: {small_font.size}px")

    # NumPy 配列として取得（ゼロコピー）
    bgra = img.asarray()  # (H, W, 4) uint8 (BGRA)

    # raw-player で表示
    player = VideoPlayer(width=w, height=h, title="Text Rendering (macOS only)")
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
