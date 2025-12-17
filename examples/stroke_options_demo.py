#!/usr/bin/env python3
"""
Stroke Options デモ

線のキャップ (cap)、結合 (join)、miter limit の設定を示すサンプルです。
"""

import math

from blend2d import CompOp, Context, Image, Path, StrokeCap, StrokeJoin
from raw_player import VideoPlayer


def main():
    w, h = 900, 700

    img = Image(w, h)

    with Context(img) as ctx:
        # 背景を白で塗りつぶし
        ctx.set_fill_style_rgba(255, 255, 255, 255)
        ctx.fill_all()

        ctx.set_comp_op(CompOp.SRC_OVER)
        ctx.set_stroke_style_rgba(0, 0, 0, 255)
        ctx.set_stroke_width(20.0)

        # === Line Cap のデモ ===
        y = 80.0

        # BUTT (デフォルト)
        ctx.set_stroke_caps(StrokeCap.BUTT)
        path = Path()
        path.move_to(50.0, y)
        path.line_to(250.0, y)
        ctx.stroke_path(path)
        ctx.set_fill_style_rgba(255, 0, 0, 255)
        ctx.set_stroke_width(1.0)
        ctx.set_stroke_style_rgba(255, 0, 0, 255)
        ctx.stroke_rect(50.0 - 2.0, y - 15.0, 4.0, 30.0)  # 開始位置のマーカー
        ctx.stroke_rect(250.0 - 2.0, y - 15.0, 4.0, 30.0)  # 終了位置のマーカー
        ctx.set_stroke_style_rgba(0, 0, 0, 255)
        ctx.set_stroke_width(20.0)

        # SQUARE
        y += 80.0
        ctx.set_stroke_caps(StrokeCap.SQUARE)
        path = Path()
        path.move_to(50.0, y)
        path.line_to(250.0, y)
        ctx.stroke_path(path)
        ctx.set_stroke_width(1.0)
        ctx.set_stroke_style_rgba(255, 0, 0, 255)
        ctx.stroke_rect(50.0 - 2.0, y - 15.0, 4.0, 30.0)
        ctx.stroke_rect(250.0 - 2.0, y - 15.0, 4.0, 30.0)
        ctx.set_stroke_style_rgba(0, 0, 0, 255)
        ctx.set_stroke_width(20.0)

        # ROUND
        y += 80.0
        ctx.set_stroke_caps(StrokeCap.ROUND)
        path = Path()
        path.move_to(50.0, y)
        path.line_to(250.0, y)
        ctx.stroke_path(path)
        ctx.set_stroke_width(1.0)
        ctx.set_stroke_style_rgba(255, 0, 0, 255)
        ctx.stroke_rect(50.0 - 2.0, y - 15.0, 4.0, 30.0)
        ctx.stroke_rect(250.0 - 2.0, y - 15.0, 4.0, 30.0)
        ctx.set_stroke_style_rgba(0, 0, 0, 255)
        ctx.set_stroke_width(20.0)

        # === Line Join のデモ ===
        x_offset = 350.0
        y = 80.0

        # MITER_CLIP (デフォルト)
        ctx.set_stroke_caps(StrokeCap.BUTT)
        ctx.set_stroke_join(StrokeJoin.MITER_CLIP)
        ctx.set_stroke_miter_limit(4.0)
        path = Path()
        path.move_to(x_offset, y)
        path.line_to(x_offset + 100.0, y)
        path.line_to(x_offset + 100.0, y + 50.0)
        ctx.stroke_path(path)

        # BEVEL
        y += 100.0
        ctx.set_stroke_join(StrokeJoin.BEVEL)
        path = Path()
        path.move_to(x_offset, y)
        path.line_to(x_offset + 100.0, y)
        path.line_to(x_offset + 100.0, y + 50.0)
        ctx.stroke_path(path)

        # ROUND
        y += 100.0
        ctx.set_stroke_join(StrokeJoin.ROUND)
        path = Path()
        path.move_to(x_offset, y)
        path.line_to(x_offset + 100.0, y)
        path.line_to(x_offset + 100.0, y + 50.0)
        ctx.stroke_path(path)

        # === Miter Limit のデモ ===
        x_offset = 650.0
        y = 80.0

        # Miter Limit = 2.0 (小さい)
        ctx.set_stroke_join(StrokeJoin.MITER_CLIP)
        ctx.set_stroke_miter_limit(2.0)
        path = Path()
        path.move_to(x_offset, y + 40.0)
        path.line_to(x_offset + 50.0, y)
        path.line_to(x_offset + 100.0, y + 40.0)
        ctx.stroke_path(path)

        # Miter Limit = 10.0 (大きい)
        y += 100.0
        ctx.set_stroke_miter_limit(10.0)
        path = Path()
        path.move_to(x_offset, y + 40.0)
        path.line_to(x_offset + 50.0, y)
        path.line_to(x_offset + 100.0, y + 40.0)
        ctx.stroke_path(path)

        # === 複雑な図形での組み合わせ ===
        y = 500.0
        ctx.set_stroke_width(15.0)
        ctx.set_stroke_style_rgba(0, 100, 200, 255)

        # 星型 - ROUND cap + ROUND join
        ctx.set_stroke_caps(StrokeCap.ROUND)
        ctx.set_stroke_join(StrokeJoin.ROUND)

        path = Path()
        cx, cy = 150.0, y + 80.0
        r_outer, r_inner = 60.0, 25.0
        points = 5

        for i in range(points * 2):
            angle = math.pi * 2 * i / (points * 2) - math.pi / 2
            r = r_outer if i % 2 == 0 else r_inner
            x = cx + r * math.cos(angle)
            y_pos = cy + r * math.sin(angle)

            if i == 0:
                path.move_to(x, y_pos)
            else:
                path.line_to(x, y_pos)
        path.close()

        ctx.stroke_path(path)

        # 星型 - BUTT cap + MITER_CLIP join
        ctx.set_stroke_caps(StrokeCap.BUTT)
        ctx.set_stroke_join(StrokeJoin.MITER_CLIP)
        ctx.set_stroke_miter_limit(4.0)
        ctx.set_stroke_style_rgba(200, 100, 0, 255)

        path = Path()
        cx = 450.0

        for i in range(points * 2):
            angle = math.pi * 2 * i / (points * 2) - math.pi / 2
            r = r_outer if i % 2 == 0 else r_inner
            x = cx + r * math.cos(angle)
            y_pos = cy + r * math.sin(angle)

            if i == 0:
                path.move_to(x, y_pos)
            else:
                path.line_to(x, y_pos)
        path.close()

        ctx.stroke_path(path)

        # 星型 - SQUARE cap + BEVEL join
        ctx.set_stroke_caps(StrokeCap.SQUARE)
        ctx.set_stroke_join(StrokeJoin.BEVEL)
        ctx.set_stroke_style_rgba(0, 150, 0, 255)

        path = Path()
        cx = 750.0

        for i in range(points * 2):
            angle = math.pi * 2 * i / (points * 2) - math.pi / 2
            r = r_outer if i % 2 == 0 else r_inner
            x = cx + r * math.cos(angle)
            y_pos = cy + r * math.sin(angle)

            if i == 0:
                path.move_to(x, y_pos)
            else:
                path.line_to(x, y_pos)
        path.close()

        ctx.stroke_path(path)

    # NumPy 配列として取得
    bgra = img.asarray()

    # raw-player で表示
    player = VideoPlayer(width=w, height=h, title="Stroke Options Demo")
    player.enqueue_video_bgra(bgra, 0)

    # キーコールバックを設定（ESC または q で終了）
    def on_key(key: int) -> bool:
        if key == 27 or key == 113:  # ESC or 'q'
            return False
        return True

    player.set_key_callback(on_key)
    player.play()

    print("Stroke Options デモ")
    print("")
    print("=== Line Cap (左上) ===")
    print("1. BUTT: 線の端が切り取られる (デフォルト)")
    print("2. SQUARE: 線の端が四角く伸びる")
    print("3. ROUND: 線の端が丸くなる")
    print("")
    print("=== Line Join (中央上) ===")
    print("1. MITER_CLIP: 尖った結合 (デフォルト)")
    print("2. BEVEL: 斜めに切り取られた結合")
    print("3. ROUND: 丸い結合")
    print("")
    print("=== Miter Limit (右上) ===")
    print("1. 小さい値 (2.0): 鋭角が制限される")
    print("2. 大きい値 (10.0): 鋭角が伸びる")
    print("")
    print("=== 複雑な図形 (下) ===")
    print("星型に異なる cap と join を適用")
    print("")
    print("ESC または q キーで終了します...")

    while player.is_open:
        if not player.poll_events():
            break

    player.close()
    print("終了します...")


if __name__ == "__main__":
    main()
