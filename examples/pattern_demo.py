#!/usr/bin/env python3
"""
Pattern デモ

Image をテクスチャとして使用するパターン塗りつぶしのサンプルです。
"""

import cv2

from blend2d import CompOp, Context, ExtendMode, Image, Pattern


def create_checkerboard_pattern(size: int, color1: tuple, color2: tuple) -> Image:
    """チェック柄のパターン Image を作成"""
    img = Image(size, size)

    with Context(img) as ctx:
        # 4x4 のチェック柄
        half = size // 2
        ctx.set_fill_style_rgba(*color1)
        ctx.fill_rect(0.0, 0.0, float(half), float(half))
        ctx.fill_rect(float(half), float(half), float(half), float(half))

        ctx.set_fill_style_rgba(*color2)
        ctx.fill_rect(float(half), 0.0, float(half), float(half))
        ctx.fill_rect(0.0, float(half), float(half), float(half))

    return img


def create_gradient_pattern(size: int) -> Image:
    """グラデーションパターン Image を作成"""
    img = Image(size, size)

    with Context(img) as ctx:
        # 左から右へのグラデーション風
        for i in range(size):
            r = int(255 * i / size)
            g = 128
            b = int(255 * (1 - i / size))
            ctx.set_fill_style_rgba(r, g, b, 255)
            ctx.fill_rect(float(i), 0.0, 1.0, float(size))

    return img


def main():
    w, h = 800, 600

    img = Image(w, h)

    with Context(img) as ctx:
        # 背景を白で塗りつぶし
        ctx.set_fill_style_rgba(255, 255, 255, 255)
        ctx.fill_all()

        ctx.set_comp_op(CompOp.SRC_OVER)

        # 1. チェック柄パターン (REPEAT モード)
        checker_img = create_checkerboard_pattern(32, (255, 100, 100, 255), (100, 100, 255, 255))
        pattern1 = Pattern()
        pattern1.create(checker_img, ExtendMode.REPEAT)

        ctx.set_fill_style_pattern(pattern1)
        ctx.fill_rect(50.0, 50.0, 300.0, 200.0)

        # 2. グラデーションパターン (REPEAT モード)
        grad_img = create_gradient_pattern(64)
        pattern2 = Pattern()
        pattern2.create(grad_img, ExtendMode.REPEAT)

        ctx.set_fill_style_pattern(pattern2)
        ctx.fill_circle(550.0, 150.0, 100.0)

        # 3. チェック柄パターンを円に適用 (PAD モード)
        pattern3 = Pattern()
        pattern3.create(checker_img, ExtendMode.PAD)

        ctx.set_fill_style_pattern(pattern3)
        ctx.fill_circle(200.0, 450.0, 80.0)

        # 4. パターンの一部を使用 (area 指定)
        pattern4 = Pattern()
        pattern4.create(checker_img, ExtendMode.REPEAT)
        pattern4.set_area(0, 0, 16, 16)  # 左上の 1/4 だけを使用

        ctx.set_fill_style_pattern(pattern4)
        ctx.fill_rect(450.0, 350.0, 300.0, 200.0)

    # NumPy 配列として取得
    rgba = img.asarray()

    # OpenCV で表示（BGRA → BGR 変換）
    bgr = cv2.cvtColor(rgba, cv2.COLOR_BGRA2BGR)
    cv2.imshow("Pattern Demo", bgr)

    print("Pattern デモ")
    print("1. 左上: チェック柄パターン (REPEAT)")
    print("2. 右上: グラデーションパターンの円 (REPEAT)")
    print("3. 左下: チェック柄パターンの円 (PAD)")
    print("4. 右下: パターンの一部を使用 (area 指定)")
    print("")
    print("何かキーを押すと終了します...")

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
