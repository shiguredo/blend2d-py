from ._blend2d import (
    version as _native_version,
    Image,
    Context,
    Path,
    CompOp,
)

__all__ = [
    "version",
    "Image",
    "Context",
    "Path",
    "CompOp",
]

def version() -> str:
    """バインディングのバージョン/存在確認用。"""
    return _native_version()
