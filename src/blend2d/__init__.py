from .blend2d_ext import (
    version as _native_version,
    Image,
    Context,
    Path,
    CompOp,
    ExtendMode,
    GradientType,
    Gradient,
    Pattern,
    StrokeCap,
    StrokeJoin,
    FontFace,
    Font,
)

__all__ = [
    "version",
    "Image",
    "Context",
    "Path",
    "CompOp",
    "ExtendMode",
    "GradientType",
    "Gradient",
    "Pattern",
    "StrokeCap",
    "StrokeJoin",
    "FontFace",
    "Font",
]


def version() -> str:
    """バインディングのバージョン/存在確認用。"""
    return _native_version()
