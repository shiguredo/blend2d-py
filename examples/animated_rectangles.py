"""
アニメーション版四角形

半透明の四角形が画面内を移動し、端に当たると跳ね返るアニメーションサンプルです。
"""

import random
import time

from blend2d import CompOp, Context, Image
from raw_player import VideoPlayer


class AnimatedRect:
    """アニメーションする四角形クラス"""

    def __init__(self, x, y, width, height, vx, vy, r, g, b, alpha):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vx = vx  # X方向の速度
        self.vy = vy  # Y方向の速度
        self.r = r
        self.g = g
        self.b = b
        self.alpha = alpha

    def update(self, screen_width, screen_height):
        """位置を更新し、画面端で跳ね返る"""
        self.x += self.vx
        self.y += self.vy

        # 左右の壁で跳ね返る
        if self.x <= 0 or self.x + self.width >= screen_width:
            self.vx = -self.vx
            self.x = max(0, min(self.x, screen_width - self.width))

        # 上下の壁で跳ね返る
        if self.y <= 0 or self.y + self.height >= screen_height:
            self.vy = -self.vy
            self.y = max(0, min(self.y, screen_height - self.height))

    def draw(self, ctx):
        """四角形を描画"""
        ctx.set_fill_style_rgba(self.r, self.g, self.b, self.alpha)
        ctx.fill_rect(self.x, self.y, self.width, self.height)


def main():
    w, h = 640, 480
    fps = 120

    # アニメーションする四角形を作成（ランダムサイズ）
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
    ]

    rects = []
    for i, color in enumerate(colors):
        x = random.randint(50, w - 150)
        y = random.randint(50, h - 150)
        width = random.randint(40, 160)  # 幅を40〜160でランダム
        height = random.randint(40, 140)  # 高さを40〜140でランダム
        vx = random.uniform(-6.0, 6.0)
        vy = random.uniform(-6.0, 6.0)
        alpha = random.randint(80, 150)

        rects.append(AnimatedRect(x, y, width, height, vx, vy, *color, alpha))

    # raw-player を初期化
    player = VideoPlayer(width=w, height=h, title="Animated Rectangles")

    # キーコールバックを設定（ESC または q で終了）
    def on_key(key: int) -> bool:
        if key == 27 or key == 113:  # ESC or 'q'
            return False
        return True

    player.set_key_callback(on_key)
    player.play()

    print("ESC または q キーで終了します...")
    print("半透明の四角形が画面内を移動し、壁で跳ね返ります")

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
                # 背景を暗い灰色で塗りつぶし
                ctx.set_fill_style_rgba(30, 30, 30, 255)
                ctx.fill_all()

                # 枠線を描画
                ctx.set_comp_op(CompOp.SRC_OVER)
                ctx.set_fill_style_rgba(100, 100, 100, 255)
                # 上の枠
                ctx.fill_rect(0, 0, w, 2)
                # 下の枠
                ctx.fill_rect(0, h - 2, w, 2)
                # 左の枠
                ctx.fill_rect(0, 0, 2, h)
                # 右の枠
                ctx.fill_rect(w - 2, 0, 2, h)

                # アルファブレンディングを有効化
                ctx.set_comp_op(CompOp.SRC_OVER)

                # 各四角形を更新して描画
                for rect in rects:
                    rect.update(w, h)
                    rect.draw(ctx)

            # NumPy 配列として取得
            bgra = img.asarray()

            # raw-player で表示
            pts_us = int(frame_count * 1_000_000 / fps)
            player.enqueue_video_bgra(bgra, pts_us)

            frame_count += 1
    except KeyboardInterrupt:
        pass

    player.close()
    print("終了します...")


if __name__ == "__main__":
    main()
