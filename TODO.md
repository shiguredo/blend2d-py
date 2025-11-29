# blend2d-py TODO リスト

blend2d の Python バインディングで未実装の機能を優先度順に整理。

## 凡例

- [ ] 未実装
- [x] 実装済み
- [~] 実装中

---

## 最優先: 描画に不可欠な機能


### 3. Context の変換機能 (追加)

現在 translate(), rotate() のみ実装。以下を追加:

- [ ] scale(x, y) / scale(xy)
- [ ] skew(x, y)
- [ ] reset_transform()
- [ ] rotate_around(angle, x, y)
- [ ] transform(matrix) - Matrix2D 適用
- [ ] post_translate, post_scale, post_skew, post_rotate

### Matrix2D (変換行列)

- [ ] Matrix2D クラス
  - [ ] create (identity, translation, scaling, rotation)
  - [ ] reset, reset_to_xxx
  - [ ] translate, scale, rotate, skew
  - [ ] transform (matrix 適用)
  - [ ] invert
  - [ ] map_point, map_vector
- [ ] Context での Matrix 対応
  - [ ] set_transform (直接設定)
  - [ ] apply_transform (追加適用)
  - [ ] get_transform (取得)

### 4. Stroke (線描画) - 部分実装

- [ ] Context の Stroke メソッド (未実装)
  - [ ] stroke_geometry
  - [ ] stroke_utf8_text
- [ ] StrokeOptions (未実装)
  - [ ] dash_array (破線パターン)
  - [ ] dash_offset
  - [ ] transform_order
  - [ ] set_stroke_options (StrokeOptions 構造体を直接設定)

### 5. Path の曲線機能

- [x] ベジェ曲線
  - [x] quad_to (二次ベジェ)
  - [x] cubic_to (三次ベジェ)
  - [x] smooth_quad_to
  - [x] smooth_cubic_to
  - [ ] conic_to (円錐曲線)
- [x] 円弧
  - [x] arc_to
  - [x] elliptic_arc_to
  - [ ] arc_quadrant_to
- [ ] ジオメトリ追加
  - [ ] add_rect, add_box
  - [ ] add_circle, add_ellipse
  - [ ] add_round_rect
  - [ ] add_arc, add_chord, add_pie
  - [ ] add_line, add_triangle
  - [ ] add_polygon, add_polyline
  - [ ] add_path

### 6. Context の Blit 機能

- [ ] blit_image
  - [ ] 基本的な blit (位置指定)
  - [ ] src rect 指定
- [ ] blit_scaled_image
  - [ ] スケーリング指定
  - [ ] src/dst rect 指定

### 7. Context の Clip 機能

- [ ] clear_all
- [ ] clear_rect
- [ ] clip_to_rect
- [ ] restore_clipping

---

## 高優先度: 実用的な描画に必要

### 8. Image I/O

- [ ] read_from_file
  - [ ] 基本的な読み込み
  - [ ] codec 指定
- [ ] write_to_file
  - [ ] 基本的な書き込み
  - [ ] codec 指定
- [ ] read_from_data (メモリバッファ)
- [ ] write_to_data (メモリバッファ)

### 9. Image の変換機能

- [ ] scale
  - [ ] NEAREST フィルタ
  - [ ] BILINEAR フィルタ
  - [ ] BICUBIC フィルタ
  - [ ] LANCZOS フィルタ
- [ ] convert (フォーマット変換)
- [ ] create_from_data (外部データ)
- [ ] make_mutable

### 10. Geometry 型のサポート

- [ ] Point, PointI
- [ ] Size, SizeI
- [ ] Box, BoxI
- [ ] Rect, RectI
- [ ] Circle
- [ ] Ellipse
- [ ] RoundRect
- [ ] Arc
- [ ] Line
- [ ] Triangle

### 11. CompOp の完全サポート

現在 SRC_COPY, SRC_OVER のみ実装。以下を追加:

- [ ] SRC_IN, SRC_OUT, SRC_ATOP
- [ ] DST_COPY, DST_OVER, DST_IN, DST_OUT, DST_ATOP
- [ ] XOR
- [ ] PLUS, MINUS, MULTIPLY, SCREEN
- [ ] OVERLAY, DARKEN, LIGHTEN
- [ ] COLOR_DODGE, COLOR_BURN
- [ ] HARD_LIGHT, SOFT_LIGHT
- [ ] DIFFERENCE, EXCLUSION

### 12. Path の変換・操作

- [ ] translate (パスの移動)
- [ ] transform (変換行列適用)
- [ ] fit_to (矩形にフィット)
- [ ] reverse (パスの反転)
- [ ] add_stroked_path

### 13. Path の情報取得

- [ ] get_bounding_box
- [ ] get_control_box
- [ ] get_info_flags
- [ ] hit_test

### 14. Context の高度な機能

- [ ] fill_geometry (汎用ジオメトリ)
- [ ] stroke_geometry (汎用ジオメトリ)
- [ ] set_fill_rule (NON_ZERO, EVEN_ODD)
- [ ] set_fill_alpha
- [ ] set_stroke_alpha
- [ ] set_global_alpha
- [ ] flush
- [ ] Context Hints
  - [ ] rendering_quality
  - [ ] gradient_quality
  - [ ] pattern_quality

---

## 中優先度: 特定用途で必要

### 15. ImageCodec 関連

- [ ] ImageCodec クラス
  - [ ] built_in_codecs
  - [ ] find_by_name
  - [ ] find_by_extension
  - [ ] find_by_data
- [ ] ImageDecoder クラス
- [ ] ImageEncoder クラス

### 16. Font の高度な機能

- [ ] FontManager
  - [ ] create
  - [ ] add_face
- [ ] FontData
  - [ ] create_from_file
  - [ ] create_from_data
- [ ] FontFeatureSettings
- [ ] FontVariationSettings
- [ ] GlyphBuffer
- [ ] GlyphRun
- [ ] テキストメトリクス取得

---

## 低優先度: 特殊用途

### 17. その他のユーティリティ

- [ ] BitArray
- [ ] BitSet
- [ ] PixelConverter
- [ ] Random
- [ ] Runtime, RuntimeScope

---

## 実装済み機能

### Image (基本機能)

- [x] create (幅、高さ指定)
- [x] width, height プロパティ
- [x] memoryview() - PEP 3118 メモリビュー
- [x] asarray() - NumPy 配列変換

### Context (基本描画)

- [x] 初期化 (Image から, thread_count オプション)
- [x] end(), save(), restore()
- [x] set_comp_op() (SRC_COPY, SRC_OVER)
- [x] set_fill_style_rgba()
- [x] translate(), rotate()
- [x] fill_all()
- [x] fill_rect()
- [x] fill_circle()
- [x] fill_pie()
- [x] fill_path()
- [x] fill_utf8_text()

### Path (基本機能)

- [x] move_to()
- [x] line_to()
- [x] quad_to() (二次ベジェ曲線)
- [x] cubic_to() (三次ベジェ曲線)
- [x] smooth_quad_to()
- [x] smooth_cubic_to()
- [x] arc_to() (円弧)
- [x] elliptic_arc_to() (楕円弧)
- [x] close()

### Font 関連

- [x] FontFace: create_from_file(), family_name, weight
- [x] Font: create_from_face(), size

### Gradient (グラデーション)

- [x] Gradient クラス
- [x] Linear Gradient (線形グラデーション): create_linear
- [x] Radial Gradient (放射状グラデーション): create_radial
- [x] Conic Gradient (円錐形グラデーション): create_conic
- [x] add_stop, reset_stops, stop_count
- [x] ExtendMode, GradientType 列挙型
- [x] Context: set_fill_style_gradient
- [x] Context: set_stroke_style_gradient

### Pattern (パターン)

- [x] Pattern クラス
- [x] create (Image ベース)
- [x] set_area
- [x] reset_area
- [x] set_extend_mode
- [x] extend_mode プロパティ
- [x] Context: set_fill_style_pattern
- [x] Context: set_stroke_style_pattern

### Stroke (線描画) - 部分実装

- [x] Context: set_stroke_width
- [x] Context: stroke_rect
- [x] Context: stroke_circle
- [x] Context: stroke_path
- [x] StrokeCap enum: BUTT, SQUARE, ROUND, ROUND_REV, TRIANGLE, TRIANGLE_REV
- [x] StrokeJoin enum: MITER_CLIP, MITER_BEVEL, MITER_ROUND, BEVEL, ROUND
- [x] Context: set_stroke_miter_limit
- [x] Context: set_stroke_join
- [x] Context: set_stroke_caps

### CompOp (部分実装)

- [x] SRC_COPY
- [x] SRC_OVER
