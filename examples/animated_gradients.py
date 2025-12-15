#!/usr/bin/env python3
"""
アニメーション版グラデーション

グラデーションが回転したり色が変化するアニメーションサンプルです。
"""

import colorsys
import math
import time

from blend2d import CompOp, Context, Gradient, Image
from raw_player import VideoPlayer


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

        # 色相を変化させる (3色を120度ずつずらして配置)
        for i, offset in enumerate([0.0, 0.33, 0.66, 1.0]):
            hue = (self.color_phase / (2 * math.pi) + offset) % 1.0
            r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
            grad.add_stop(offset, int(r * 255), int(g * 255), int(b * 255))

        ctx.set_fill_style_gradient(grad)
        ctx.fill_circle(self.x, self.y, self.radius)


def main():
    w, h = 640, 480
    fps = 60

    # 各種グラデーションを作成
    linear_grad = AnimatedLinearGradient(160.0, 120.0, 150.0)
    radial_grad = AnimatedRadialGradient(480.0, 120.0, 80.0)
    conic_grad = AnimatedConicGradient(320.0, 350.0, 80.0)

    # raw-player を初期化
    player = VideoPlayer(width=w, height=h, title="Animated Gradients")

    # キーコールバックを設定（ESC または q で終了）
    def on_key(key: int) -> bool:
        if key == 27 or key == 113:  # ESC or 'q'
            return False
        return True

    player.set_key_callback(on_key)
    player.play()

    print("ESC または q キーで終了します...")
    print("グラデーションが回転・変化します")

    # フレーム生成のペーシング用
    frame_interval = 1.0 / fps
    next_frame_time = time.perf_counter()

    try:
        frame_count = 0
        while player.is_open:
            if not player.poll_events():
                break

            # 次のフレーム時刻まで待機
            now = time.perf_counter()
            if now < next_frame_time:
                time.sleep(max(0, next_frame_time - now))

            # 次のフレーム時刻を更新
            next_frame_time += frame_interval

            # 新しいフレームを作成
            img = Image(w, h)

            with Context(img) as ctx:
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

            # NumPy 配列として取得
            bgra = img.asarray()

            # raw-player で表示
            pts_us = int(frame_count * 1_000_000 / fps)
            player.enqueue_video_bgra(bgra, pts_us)

            frame_count += 1
    except KeyboardInterrupt:
        pass

    player.close()
    print(f"終了します... (総フレーム数: {frame_count})")


if __name__ == "__main__":
    main()
