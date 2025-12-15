# 変更履歴

- CHANGE
  - 後方互換性のない変更
- UPDATE
  - 後方互換性がある変更
- ADD
  - 後方互換性がある追加
- FIX
  - バグ修正

## develop

- [ADD] Python 3.13t / 3.14t (Free Threading) に対応する
  - @voluntas

### misc

- [CHANGE] examples の表示ライブラリを OpenCV から raw-player に変更する
  - @voluntas
- [CHANGE] モジュール名を `blend2d_ext` に変更する
  - @voluntas
- [UPDATE] `cmake` の最小バージョンを 4.2 に上げる
  - @voluntas

## 2025.4.0

**リリース日**:: 2025-11-30

- [UPDATE] `Gradient.gradient_type` / `Gradient.extend_mode` / `Pattern.extend_mode` の戻り値型を変更する
  - `int` から enum 型 (`GradientType` / `ExtendMode`) に変更
  - @voluntas
- [ADD] `Context` にコンテキストマネージャープロトコルを追加する
  - `with Context(img) as ctx:` で使用可能
  - `with` ブロックを抜けると自動的に `end()` が呼ばれる
  - @voluntas
- [ADD] `Context` に `thread_count` 引数を追加してマルチスレッドレンダリングを可能にする
  - `thread_count=0` (デフォルト): 同期モード (シングルスレッド)
  - `thread_count=1`: 非同期モード (追加スレッドなし)
  - `thread_count>1`: 非同期モード (thread_count - 1 個のワーカースレッド)
  - @voluntas
- [ADD] `Path` に曲線機能を追加する
  - `quad_to`: 二次ベジェ曲線
  - `cubic_to`: 三次ベジェ曲線
  - `smooth_quad_to`: スムーズ二次ベジェ曲線
  - `smooth_cubic_to`: スムーズ三次ベジェ曲線
  - `arc_to`: 円弧
  - `elliptic_arc_to`: 楕円弧
  - @voluntas
- [UPDATE] `PyImage::asarray()` で `nb::ndarray` を直接使用する
  - 戻り値型を `nb::object` から `nb::ndarray<nb::numpy, uint8_t>` に変更する
  - `nanobind の ndarray` を直接使用する
  - 手動の `nb::sig` を削除してスタブ自動生成に任せる
  - @voluntas

## 2025.3.0

**リリース日**:: 2025-11-25

- [CHANGE] Python 3.11 のサポートを終了する
  - @voluntas
- [CHANGE] blend2d_ext に名前を変更する
  - @voluntas
- [CHANGE] `_deps` 以下の構成をバージョンありにする
  - @voluntas
- [CHANGE] `deps.json` を導入する
  - @voluntas
- [ADD] `Pattern` / `Stroke` / `Gradient` / `Text` を追加する
  - @voluntas

### misc

- [CHANGE] claude.yml の runs_os を ubuntu-slim に変更する
  - @voluntas
- [ADD] `.markdownlint.jsonc` を追加する
  - @voluntas

## 2025.2.0

**リリース日**:: 2025-11-14

- [ADD] Blend2D のバージョンを 0.21.2 に上げる
  - @voluntas
- [ADD] Python 3.14 をサポートに追加する
  - @voluntas
- [ADD] macos-26 をビルドに追加する
  - @voluntas

### misc

## 2025.1.0

**リリース日**:: 2025-09-10

**祝いリリース**
