#!/usr/bin/env python3
"""
アニメーション版グラデーション

グラデーションが回転したり色が変化するアニメーションサンプルです。
"""

import math

import cv2

from blend2d import CompOp, Context, Gradient, Image


class AnimatedLinearGradient:
    """アニメーションする線形グラデーション"""

    def __init__(self, x, y, length):
        self.x = x
        self.y = y
        self.length = length
        self.angle = 0.0

    def update(self):
        """角度を更新"""
        self.angle += 0.02

    def draw(self, ctx):
        """グラデーションを描画"""
        # 角度に基づいて終点を計算
        x1 = self.x + math.cos(self.angle) * self.length
        y1 = self.y + math.sin(self.angle) * self.length

        grad = Gradient()
        grad.create_linear(self.x, self.y, x1, y1)
        grad.add_stop(0.0, 255, 0, 0)  # 赤
        grad.add_stop(0.5, 0, 255, 0)  # 緑
        grad.add_stop(1.0, 0, 0, 255)  # 青

        ctx.set_fill_style_gradient(grad)
        ctx.fill_rect(self.x - 100.0, self.y - 50.0, 200.0, 100.0)


class AnimatedRadialGradient:
    """アニメーションする放射状グラデーション"""

    def __init__(self, x, y, max_radius):
        self.x = x
        self.y = y
        self.max_radius = max_radius
        self.phase = 0.0

    def update(self):
        """位相を更新"""
        self.phase += 0.05

    def draw(self, ctx):
        """グラデーションを描画"""
        # 半径を sin 波で変化させる
        radius = self.max_radius * (0.5 + 0.5 * math.sin(self.phase))

        grad = Gradient()
        grad.create_radial(self.x, self.y, self.x, self.y, radius)
        grad.add_stop(0.0, 255, 255, 0)  # 黄色
        grad.add_stop(1.0, 255, 0, 255)  # マゼンタ

        ctx.set_fill_style_gradient(grad)
        ctx.fill_circle(self.x, self.y, self.max_radius)


class AnimatedConicGradient:
    """アニメーションする円錐形グラデーション"""

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.angle = 0.0
        self.color_phase = 0.0

    def update(self):
        """角度と色を更新"""
        self.angle += 0.03
        self.color_phase += 0.02

    def draw(self, ctx):
        """グラデーションを描画"""
        grad = Gradient()
        grad.create_conic(self.x, self.y, self.angle)

        # 色相を変化させる
        r1 = int(128 + 127 * math.sin(self.color_phase))
        g1 = int(128 + 127 * math.sin(self.color_phase + 2.0))
        b1 = int(128 + 127 * math.sin(self.color_phase + 4.0))

        grad.add_stop(0.0, r1, g1, b1)
        grad.add_stop(0.33, b1, r1, g1)
        grad.add_stop(0.66, g1, b1, r1)
        grad.add_stop(1.0, r1, g1, b1)

        ctx.set_fill_style_gradient(grad)
        ctx.fill_circle(self.x, self.y, self.radius)


def main():
    w, h = 640, 480

    # 各種グラデーションを作成
    linear_grad = AnimatedLinearGradient(160.0, 120.0, 150.0)
    radial_grad = AnimatedRadialGradient(480.0, 120.0, 80.0)
    conic_grad = AnimatedConicGradient(320.0, 350.0, 80.0)

    print("Ctrl-C で終了します...")
    print("グラデーションが回転・変化します")

    try:
        frame_count = 0
        while True:
            # 新しいフレームを作成
            img = Image(w, h)
            ctx = Context(img)

            # 背景を白で塗りつぶし
            ctx.set_fill_style_rgba(255, 255, 255, 255)
            ctx.fill_all()

            # アルファブレンディングを有効化
            ctx.set_comp_op(CompOp.SRC_OVER)

            # 各グラデーションを更新して描画
            linear_grad.update()
            linear_grad.draw(ctx)

            radial_grad.update()
            radial_grad.draw(ctx)

            conic_grad.update()
            conic_grad.draw(ctx)

            ctx.end()

            # NumPy 配列として取得
            rgba = img.asarray()

            # OpenCV で表示（BGRA → BGR 変換）
            bgr = cv2.cvtColor(rgba, cv2.COLOR_BGRA2BGR)
            cv2.imshow("Animated Gradients", bgr)

            # 60 FPS で表示
            if cv2.waitKey(16) & 0xFF == ord("q"):
                break

            frame_count += 1
    except KeyboardInterrupt:
        print("\n終了します...")
    finally:
        cv2.destroyAllWindows()
        print(f"総フレーム数: {frame_count}")


if __name__ == "__main__":
    main()
