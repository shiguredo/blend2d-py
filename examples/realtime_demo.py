"""
リアルタイム描画デモ

Blend2D でリアルタイムに図形とテキストを描画し、OpenCV で表示するサンプルです。
7 セグメント風のデジタル時計、回転する円弧、横に流れるカラーボックスを描画します。
"""

import time
from math import pi, sin

import cv2

from blend2d import CompOp, Context, Image, Path


def draw_7segment(ctx: Context, digit: int, x: float, y: float, w: float, h: float) -> None:
    # 7 セグメント (a,b,c,d,e,f,g)
    #  aaa
    # f   b
    #  ggg
    # e   c
    #  ddd
    if digit < 0 or digit > 9:
        return

    thickness = w * 0.15
    gap = thickness * 0.2

    segments = [
        # a,    b,     c,     d,     e,     f,     g
        [True, True, True, True, True, True, False],  # 0
        [False, True, True, False, False, False, False],  # 1
        [True, True, False, True, True, False, True],  # 2
        [True, True, True, True, False, False, True],  # 3
        [False, True, True, False, False, True, True],  # 4
        [True, False, True, True, False, True, True],  # 5
        [True, False, True, True, True, True, True],  # 6
        [True, True, True, False, False, False, False],  # 7
        [True, True, True, True, True, True, True],  # 8
        [True, True, True, True, False, True, True],  # 9
    ]

    def draw_h(sx: float, sy: float) -> None:
        p = Path()
        p.move_to(sx + gap, sy)
        p.line_to(sx + w - gap, sy)
        p.line_to(sx + w - gap - thickness * 0.5, sy + thickness * 0.5)
        p.line_to(sx + w - gap, sy + thickness)
        p.line_to(sx + gap, sy + thickness)
        p.line_to(sx + gap + thickness * 0.5, sy + thickness * 0.5)
        p.close()
        ctx.fill_path(p)

    def draw_v(sx: float, sy: float, sh: float) -> None:
        p = Path()
        p.move_to(sx, sy + gap)
        p.line_to(sx + thickness * 0.5, sy + gap + thickness * 0.5)
        p.line_to(sx + thickness, sy + gap)
        p.line_to(sx + thickness, sy + sh - gap)
        p.line_to(sx + thickness * 0.5, sy + sh - gap - thickness * 0.5)
        p.line_to(sx, sy + sh - gap)
        p.close()
        ctx.fill_path(p)

    on = segments[digit]
    if on[0]:
        draw_h(x, y)
    if on[1]:
        draw_v(x + w - thickness, y, h * 0.5)
    if on[2]:
        draw_v(x + w - thickness, y + h * 0.5, h * 0.5)
    if on[3]:
        draw_h(x, y + h - thickness)
    if on[4]:
        draw_v(x, y + h * 0.5, h * 0.5)
    if on[5]:
        draw_v(x, y, h * 0.5)
    if on[6]:
        draw_h(x, y + h * 0.5 - thickness * 0.5)


def draw_colon(ctx: Context, x: float, y: float, h: float) -> None:
    dot = h * 0.1
    ctx.fill_circle(x + dot, y + h * 0.3, dot)
    ctx.fill_circle(x + dot, y + h * 0.7, dot)


def draw_digital_clock(ctx: Context, start_time: float, width: int, height: int) -> None:
    ms = int((time.perf_counter() - start_time) * 1000)
    hours = (ms // (60 * 60 * 1000)) % 10000
    minutes = (ms // (60 * 1000)) % 60
    seconds = (ms // 1000) % 60
    milliseconds = ms % 1000

    clock_x = width * 0.02
    clock_y = height * 0.02
    digit_w = width * 0.018
    digit_h = height * 0.04
    spacing = digit_w * 0.3
    colon_w = digit_w * 0.3

    x = clock_x
    ctx.set_fill_style_rgba(0, 255, 255)
    # HHHH
    draw_7segment(ctx, (hours // 1000) % 10, x, clock_y, digit_w, digit_h)
    x += digit_w + spacing
    draw_7segment(ctx, (hours // 100) % 10, x, clock_y, digit_w, digit_h)
    x += digit_w + spacing
    draw_7segment(ctx, (hours // 10) % 10, x, clock_y, digit_w, digit_h)
    x += digit_w + spacing
    draw_7segment(ctx, hours % 10, x, clock_y, digit_w, digit_h)
    x += digit_w + spacing

    # :
    draw_colon(ctx, x, clock_y, digit_h)
    x += colon_w + spacing

    # MM
    draw_7segment(ctx, (minutes // 10) % 10, x, clock_y, digit_w, digit_h)
    x += digit_w + spacing
    draw_7segment(ctx, minutes % 10, x, clock_y, digit_w, digit_h)
    x += digit_w + spacing

    # :
    draw_colon(ctx, x, clock_y, digit_h)
    x += colon_w + spacing

    # SS
    draw_7segment(ctx, (seconds // 10) % 10, x, clock_y, digit_w, digit_h)
    x += digit_w + spacing
    draw_7segment(ctx, seconds % 10, x, clock_y, digit_w, digit_h)
    x += digit_w + spacing

    # .
    ctx.fill_circle(x + colon_w * 0.3, clock_y + digit_h * 0.8, digit_h * 0.05)
    x += colon_w + spacing

    # mmm (smaller)
    ms_w = digit_w * 0.7
    ms_h = digit_h * 0.7
    ctx.set_fill_style_rgba(200, 200, 200)
    y_off = (digit_h - ms_h) / 2
    draw_7segment(ctx, (milliseconds // 100) % 10, x, clock_y + y_off, ms_w, ms_h)
    x += ms_w + spacing * 0.8
    draw_7segment(ctx, (milliseconds // 10) % 10, x, clock_y + y_off, ms_w, ms_h)
    x += ms_w + spacing * 0.8
    draw_7segment(ctx, milliseconds % 10, x, clock_y + y_off, ms_w, ms_h)


def main(width: int = 640, height: int = 360, fps: int = 60):
    img = Image(width, height)
    start = time.perf_counter()
    frame = 0
    win = "blend2d"
    cv2.namedWindow(win, cv2.WINDOW_AUTOSIZE)

    print("Ctrl-C で終了します...")
    try:
        while True:
            now = time.perf_counter()
            # 1フレーム描画
            ctx = Context(img)
            ctx.set_comp_op(CompOp.SRC_COPY)
            ctx.set_fill_style_rgba(0, 0, 0, 255)
            ctx.fill_all()

            # デジタル時計
            ctx.save()
            draw_digital_clock(ctx, start, width, height)
            ctx.restore()

            # 回転する円弧
            ctx.save()
            ctx.translate(width * 0.5, height * 0.5)
            ctx.rotate(-pi / 2)
            ctx.set_fill_style_rgba(255, 255, 255)
            ctx.fill_pie(0, 0, min(width, height) * 0.3, 0, 2 * pi)
            ctx.set_fill_style_rgba(160, 160, 160)
            sweep = (frame % fps) / float(fps) * 2 * pi
            ctx.fill_pie(0, 0, min(width, height) * 0.3, 0, sweep)
            ctx.restore()

            # 横に流れるボックス
            box = 50
            colors = [
                (255, 0, 0),
                (0, 255, 0),
                (0, 0, 255),
                (255, 255, 0),
                (255, 0, 255),
            ]
            for i in range(5):
                phase = (frame + i * 20) % 100 / 100.0
                x = phase * (width - box)
                y = height * 0.5 + sin(phase * 2 * pi) * height * 0.2
                r, g, b = colors[i % len(colors)]
                ctx.set_fill_style_rgba(r, g, b)
                ctx.fill_rect(x, y, box, box)

            ctx.end()

            # 表示 (PRGB32 ~ BGRA を BGR に変換)
            rgba = img.asarray()
            bgr = cv2.cvtColor(rgba, cv2.COLOR_BGRA2BGR)
            cv2.imshow(win, bgr)

            # イベント処理とフレームレート調整
            cv2.waitKey(1)
            frame += 1
            dt = time.perf_counter() - now
            wait = max(0.0, 1.0 / fps - dt)
            if wait:
                time.sleep(wait)
    except KeyboardInterrupt:
        print("\n終了します...")
    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
