import math

import blend2d as bl


def test_path_quad_to():
    """二次ベジェ曲線"""
    img = bl.Image(100, 100)
    ctx = bl.Context(img)
    path = bl.Path()
    path.move_to(10, 50)
    path.quad_to(50, 10, 90, 50)
    ctx.set_fill_style_rgba(255, 0, 0)
    ctx.fill_path(path)
    ctx.end()


def test_path_cubic_to():
    """三次ベジェ曲線"""
    img = bl.Image(100, 100)
    ctx = bl.Context(img)
    path = bl.Path()
    path.move_to(10, 50)
    path.cubic_to(30, 10, 70, 10, 90, 50)
    ctx.set_fill_style_rgba(0, 255, 0)
    ctx.fill_path(path)
    ctx.end()


def test_path_smooth_quad_to():
    """スムーズ二次ベジェ曲線"""
    img = bl.Image(100, 100)
    ctx = bl.Context(img)
    path = bl.Path()
    path.move_to(10, 50)
    path.quad_to(30, 10, 50, 50)
    path.smooth_quad_to(90, 50)
    ctx.set_fill_style_rgba(0, 0, 255)
    ctx.fill_path(path)
    ctx.end()


def test_path_smooth_cubic_to():
    """スムーズ三次ベジェ曲線"""
    img = bl.Image(100, 100)
    ctx = bl.Context(img)
    path = bl.Path()
    path.move_to(10, 50)
    path.cubic_to(20, 10, 40, 10, 50, 50)
    path.smooth_cubic_to(80, 50, 90, 50)
    ctx.set_fill_style_rgba(255, 255, 0)
    ctx.fill_path(path)
    ctx.end()


def test_path_arc_to():
    """円弧"""
    img = bl.Image(100, 100)
    ctx = bl.Context(img)
    path = bl.Path()
    path.move_to(50, 30)
    path.arc_to(50, 50, 20, 20, 0, math.pi)
    ctx.set_fill_style_rgba(255, 0, 255)
    ctx.fill_path(path)
    ctx.end()


def test_path_arc_to_with_force_move():
    """円弧 (force_move_to=True)"""
    img = bl.Image(100, 100)
    ctx = bl.Context(img)
    path = bl.Path()
    path.arc_to(50, 50, 20, 20, 0, math.pi, force_move_to=True)
    ctx.set_fill_style_rgba(255, 128, 0)
    ctx.fill_path(path)
    ctx.end()


def test_path_elliptic_arc_to():
    """楕円弧"""
    img = bl.Image(100, 100)
    ctx = bl.Context(img)
    path = bl.Path()
    path.move_to(30, 50)
    path.elliptic_arc_to(20, 10, 0, True, True, 70, 50)
    ctx.set_fill_style_rgba(0, 255, 255)
    ctx.fill_path(path)
    ctx.end()
