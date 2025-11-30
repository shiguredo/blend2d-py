#!/usr/bin/env python3
"""
コーデックテスト用アニメーション

ビットレート負荷が高い映像を生成します。
- 黒背景に軽いノイズ
- 複数のカラフルな図形（四角・円）が異なる速度・方向で動く
- 動き予測が難しく、空間周波数が揺らぐ
"""

import random

import cv2
import numpy as np

from blend2d import CompOp, Context, Image


class MovingShape:
    """アニメーションする図形の基底クラス"""

    def __init__(self, x, y, vx, vy, r, g, b, alpha):
        self.x = x
        self.y = y
        self.vx = vx  # X 方向の速度
        self.vy = vy  # Y 方向の速度
        self.r = r
        self.g = g
        self.b = b
        self.alpha = alpha
        # 速度を少しずつ変化させるためのパラメータ
        self.vx_noise = random.uniform(-0.2, 0.2)
        self.vy_noise = random.uniform(-0.2, 0.2)

    def update(self, screen_width, screen_height, frame):
        """位置を更新し、画面端で跳ね返る。速度も微妙に変化させる"""
        # ノイズを加えて速度を変化させる（ビットレート負荷を高める）
        noise_factor = 0.1 * np.sin(frame * 0.05)
        self.vx += self.vx_noise * noise_factor
        self.vy += self.vy_noise * noise_factor

        # 速度を制限
        max_speed = 10.0
        self.vx = max(-max_speed, min(max_speed, self.vx))
        self.vy = max(-max_speed, min(max_speed, self.vy))

        self.x += self.vx
        self.y += self.vy

    def check_bounds(self, screen_width, screen_height):
        """サブクラスで実装"""
        pass

    def draw(self, ctx):
        """サブクラスで実装"""
        pass


class MovingRect(MovingShape):
    """アニメーションする四角形"""

    def __init__(self, x, y, width, height, vx, vy, r, g, b, alpha):
        super().__init__(x, y, vx, vy, r, g, b, alpha)
        self.width = width
        self.height = height

    def check_bounds(self, screen_width, screen_height):
        """画面端で跳ね返る"""
        if self.x <= 0 or self.x + self.width >= screen_width:
            self.vx = -self.vx
            self.x = max(0.0, min(self.x, screen_width - self.width))

        if self.y <= 0 or self.y + self.height >= screen_height:
            self.vy = -self.vy
            self.y = max(0.0, min(self.y, screen_height - self.height))

    def draw(self, ctx):
        """四角形を描画"""
        ctx.set_fill_style_rgba(self.r, self.g, self.b, self.alpha)
        ctx.fill_rect(self.x, self.y, self.width, self.height)


class MovingCircle(MovingShape):
    """アニメーションする円"""

    def __init__(self, x, y, radius, vx, vy, r, g, b, alpha):
        super().__init__(x, y, vx, vy, r, g, b, alpha)
        self.radius = radius

    def check_bounds(self, screen_width, screen_height):
        """画面端で跳ね返る"""
        if self.x - self.radius <= 0 or self.x + self.radius >= screen_width:
            self.vx = -self.vx
            self.x = max(self.radius, min(self.x, screen_width - self.radius))

        if self.y - self.radius <= 0 or self.y + self.radius >= screen_height:
            self.vy = -self.vy
            self.y = max(self.radius, min(self.y, screen_height - self.radius))

    def draw(self, ctx):
        """円を描画"""
        ctx.set_fill_style_rgba(self.r, self.g, self.b, self.alpha)
        ctx.fill_circle(self.x, self.y, self.radius)


def generate_noise_cache(width, height, num_patterns=10, noise_intensity=15):
    """ノイズパターンを事前生成してキャッシュ（性能改善）"""
    cache = []
    for _ in range(num_patterns):
        noise = np.random.normal(0, noise_intensity, (height, width, 4)).astype(np.int16)
        cache.append(noise)
    return cache


def add_noise_cached(frame, noise_cache, frame_num):
    """キャッシュされたノイズを適用（高速版）"""
    noise = noise_cache[frame_num % len(noise_cache)]
    noisy_frame = np.clip(frame.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    return noisy_frame


def main(width=1280, height=720, fps=60, num_shapes=20):
    """
    コーデックテスト用アニメーション（リアルタイム表示）

    Args:
        width: 映像の幅
        height: 映像の高さ
        fps: フレームレート
        num_shapes: 図形の数
    """

    # カラフルな色のパレット
    colors = [
        (255, 0, 0),  # 赤
        (0, 255, 0),  # 緑
        (0, 0, 255),  # 青
        (255, 255, 0),  # 黄色
        (255, 0, 255),  # マゼンタ
        (0, 255, 255),  # シアン
        (255, 128, 0),  # オレンジ
        (128, 0, 255),  # 紫
        (64, 255, 64),  # 黄緑
        (255, 192, 203),  # ピンク
        (128, 128, 255),  # ライトブルー
        (255, 128, 128),  # ライトレッド
    ]

    # 図形を作成（四角と円を混在）
    shapes = []
    for i in range(num_shapes):
        x = random.randint(50, width - 150)
        y = random.randint(50, height - 150)
        vx = random.uniform(-8.0, 8.0)
        vy = random.uniform(-8.0, 8.0)
        color = random.choice(colors)
        alpha = random.randint(120, 200)

        # 50% の確率で四角または円
        if random.random() < 0.5:
            w = random.randint(40, 120)
            h = random.randint(40, 120)
            shapes.append(MovingRect(x, y, w, h, vx, vy, *color, alpha))
        else:
            r = random.randint(20, 60)
            shapes.append(MovingCircle(x, y, r, vx, vy, *color, alpha))

    print("コーデックテスト用アニメーション")
    print(f"解像度: {width}x{height}")
    print(f"FPS: {fps}")
    print(f"図形数: {num_shapes}")
    print("ノイズキャッシュを生成中...")

    # ノイズパターンを事前生成（性能改善）
    noise_cache = generate_noise_cache(width, height, num_patterns=10, noise_intensity=40)

    print("Ctrl-C または 'q' キーで終了します...")

    # Image を1回だけ作成（性能改善）
    img = Image(width, height)

    frame_num = 0
    try:
        while True:
            # 1フレーム描画
            with Context(img) as ctx:
                # 背景を黒で塗りつぶし（Image を再利用）
                ctx.set_comp_op(CompOp.SRC_COPY)
                ctx.set_fill_style_rgba(0, 0, 0, 255)
                ctx.fill_all()

                # アルファブレンディングを有効化
                ctx.set_comp_op(CompOp.SRC_OVER)

                # 各図形を更新して描画
                for shape in shapes:
                    shape.update(width, height, frame_num)
                    shape.check_bounds(width, height)
                    shape.draw(ctx)

            # NumPy 配列として取得
            rgba = img.asarray()

            # キャッシュされたノイズを適用（高速）
            rgba = add_noise_cached(rgba, noise_cache, frame_num)

            # OpenCV で表示（BGRA → BGR 変換）
            bgr = cv2.cvtColor(rgba, cv2.COLOR_BGRA2BGR)
            cv2.imshow("Codec Test Animation", bgr)

            # フレームレート調整
            if cv2.waitKey(int(1000 / fps)) & 0xFF == ord("q"):
                break

            frame_num += 1

    except KeyboardInterrupt:
        print("\n終了します...")
    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    # デフォルト設定で実行
    # 1920x1080, 60fps, 20個の図形
    main()

    # カスタム設定の例:
    # main(width=1280, height=720, fps=30, num_shapes=15)
