"""
アニメーション版四角形

半透明の四角形が画面内を移動し、端に当たると跳ね返るアニメーションサンプルです。
"""

import random

import cv2

from blend2d import CompOp, Context, Image


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

    print("Ctrl-C で終了します...")
    print("半透明の四角形が画面内を移動し、壁で跳ね返ります")

    try:
        while True:
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
            rgba = img.asarray()

            # OpenCV で表示（BGRA → BGR 変換）
            bgr = cv2.cvtColor(rgba, cv2.COLOR_BGRA2BGR)
            cv2.imshow("Animated Rectangles", bgr)

            # 120 FPS で表示
            cv2.waitKey(8)
    except KeyboardInterrupt:
        print("\n終了します...")
    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
