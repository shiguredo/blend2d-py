cmake_minimum_required(VERSION 4.1)
project(blend2d_py LANGUAGES CXX)

# プラットフォームチェック
if(NOT APPLE AND NOT UNIX AND NOT WIN32)
  message(FATAL_ERROR "This package supports macOS, Linux (Ubuntu), and Windows.")
endif()

# Python / nanobind
find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)
find_package(nanobind CONFIG REQUIRED)

include(ExternalProject)

# ソース取得（ミラー）
set(BLEND2D_URL "https://oss-mirrors.shiguredo.jp/blend2d-0.20.0.tar.gz" CACHE STRING "Blend2D source tarball URL")

# レイアウト: ダウンロードしたソースは _source 下、ビルド済み + インストール済みバイナリは _build 下
# SKBUILD_PROJECT_DIR が利用可能な場合は使用（scikit-build-core）、そうでなければ CMAKE_CURRENT_SOURCE_DIR にフォールバック
if(DEFINED SKBUILD_PROJECT_DIR)
  set(PROJECT_ROOT "${SKBUILD_PROJECT_DIR}")
else()
  set(PROJECT_ROOT "${CMAKE_CURRENT_SOURCE_DIR}")
endif()

set(BLEND2D_SOURCE_DIR "${PROJECT_ROOT}/_source/blend2d")
set(BLEND2D_BUILD_DIR  "${PROJECT_ROOT}/_build/blend2d")
set(BLEND2D_INSTALL    "${PROJECT_ROOT}/_install")

ExternalProject_Add(blend2d_ep
  URL                 ${BLEND2D_URL}
  SOURCE_DIR          ${BLEND2D_SOURCE_DIR}
  BINARY_DIR          ${BLEND2D_BUILD_DIR}/build
  STAMP_DIR           ${BLEND2D_BUILD_DIR}/stamp
  TMP_DIR             ${BLEND2D_BUILD_DIR}/tmp
  UPDATE_COMMAND      ""
  DOWNLOAD_EXTRACT_TIMESTAMP TRUE
  CMAKE_ARGS
    -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
    -DCMAKE_INSTALL_PREFIX=${BLEND2D_INSTALL}
    -DCMAKE_INSTALL_LIBDIR=lib
    -DCMAKE_POSITION_INDEPENDENT_CODE=ON
    -DBUILD_SHARED_LIBS=OFF
    -DBLEND2D_STATIC=TRUE
    -DBUILD_TESTING=OFF
  BUILD_BYPRODUCTS
    ${BLEND2D_INSTALL}/lib/libblend2d.a
    ${BLEND2D_INSTALL}/lib64/libblend2d.a
    ${BLEND2D_INSTALL}/lib/blend2d.lib
    ${BLEND2D_INSTALL}/lib/Release/blend2d.lib
    ${BLEND2D_INSTALL}/lib/Debug/blend2d.lib
)

## リンクディレクトリ経由で名前でリンク（静的/共有両方で動作）

# nanobind モジュール
nanobind_add_module(_blend2d
  NB_DOMAIN "blend2d"
  src/bindings/bind.cpp
)

add_dependencies(_blend2d blend2d_ep)
find_package(Threads)
target_include_directories(_blend2d PRIVATE ${BLEND2D_INSTALL}/include)
target_link_directories(_blend2d PRIVATE ${BLEND2D_INSTALL}/lib ${BLEND2D_INSTALL}/lib64)

# 可能なら事前にフルパスでライブラリを解決する（無ければ後段の名前解決に委ねる）
find_library(BLEND2D_LIB
  NAMES blend2d
  PATHS 
    ${BLEND2D_INSTALL}/lib 
    ${BLEND2D_INSTALL}/lib64
    ${BLEND2D_INSTALL}/lib/Release
    ${BLEND2D_INSTALL}/lib/Debug
  NO_DEFAULT_PATH
)
if(BLEND2D_LIB)
  set(BLEND2D_LINK_TARGET ${BLEND2D_LIB})
else()
  set(BLEND2D_LINK_TARGET blend2d)
  message(STATUS "blend2d ライブラリ未検出。ビルド後にリンク探索します: ${BLEND2D_INSTALL}/lib, ${BLEND2D_INSTALL}/lib64")
endif()
# プラットフォーム固有のライブラリ
if(APPLE)
  target_link_libraries(_blend2d PRIVATE ${BLEND2D_LINK_TARGET} Threads::Threads)
elseif(UNIX)
  target_link_libraries(_blend2d PRIVATE ${BLEND2D_LINK_TARGET} Threads::Threads rt)
elseif(WIN32)
  target_link_libraries(_blend2d PRIVATE ${BLEND2D_LINK_TARGET} Threads::Threads)
endif()

# コンパイルオプションとマクロ定義
# 静的ライブラリを使用しているため BL_STATIC を定義
target_compile_definitions(_blend2d PRIVATE BL_STATIC)

if(NOT WIN32)
  target_compile_options(_blend2d PRIVATE -fvisibility=hidden)
endif()

set_target_properties(_blend2d PROPERTIES OUTPUT_NAME "_blend2d")

# 型スタブ (.pyi) ファイルの自動生成
nanobind_add_stub(
  blend2d_stub
  MODULE _blend2d
  OUTPUT __init__.pyi
  PYTHON_PATH $<TARGET_FILE_DIR:_blend2d>
  DEPENDS _blend2d
  MARKER_FILE py.typed
)

# Wheel に配置するためのインストール先を指定
set(PY_PACKAGE "blend2d")
install(TARGETS _blend2d
  LIBRARY DESTINATION ${PY_PACKAGE}
  RUNTIME DESTINATION ${PY_PACKAGE}
)

# 型スタブファイルとマーカーファイルをインストール
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/__init__.pyi DESTINATION ${PY_PACKAGE})
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/py.typed DESTINATION ${PY_PACKAGE})
