import blend2d as bl


def test_context_default():
    """デフォルトの Context 作成 (シングルスレッド)"""
    img = bl.Image(100, 100)
    ctx = bl.Context(img)
    ctx.set_fill_style_rgba(255, 0, 0)
    ctx.fill_rect(0, 0, 100, 100)
    ctx.end()


def test_context_thread_count_zero():
    """thread_count=0 で Context 作成 (シングルスレッド)"""
    img = bl.Image(100, 100)
    ctx = bl.Context(img, thread_count=0)
    ctx.set_fill_style_rgba(0, 255, 0)
    ctx.fill_rect(0, 0, 100, 100)
    ctx.end()


def test_context_thread_count_multithread():
    """thread_count=4 で Context 作成 (マルチスレッド)"""
    img = bl.Image(1920, 1080)
    ctx = bl.Context(img, thread_count=4)
    ctx.set_fill_style_rgba(0, 0, 255)
    ctx.fill_rect(0, 0, 1920, 1080)
    ctx.end()


def test_context_thread_count_keyword_arg():
    """キーワード引数で thread_count を指定"""
    img = bl.Image(640, 480)
    ctx = bl.Context(image=img, thread_count=2)
    ctx.end()
