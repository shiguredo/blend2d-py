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

# レイアウト: ExternalProject の依存関係は _deps 配下で管理
# SKBUILD_PROJECT_DIR が利用可能な場合は使用（scikit-build-core）、そうでなければ CMAKE_CURRENT_SOURCE_DIR にフォールバック
if(DEFINED SKBUILD_PROJECT_DIR)
  set(PROJECT_ROOT "${SKBUILD_PROJECT_DIR}")
else()
  set(PROJECT_ROOT "${CMAKE_CURRENT_SOURCE_DIR}")
endif()

set(DEPS_DIR "${PROJECT_ROOT}/_deps")
message(STATUS "Dependencies directory: ${DEPS_DIR}")

# JSON から依存関係のバージョンを読み込み
file(READ ${CMAKE_CURRENT_SOURCE_DIR}/deps.json DEPS_JSON)

# Blend2D の設定を解析
string(JSON BLEND2D_VERSION GET ${DEPS_JSON} blend2d version)
string(JSON BLEND2D_HASH GET ${DEPS_JSON} blend2d hash)
string(JSON BLEND2D_URL GET ${DEPS_JSON} blend2d url)

set(BLEND2D_SOURCE_DIR "${DEPS_DIR}/blend2d/${BLEND2D_VERSION}/source")
set(BLEND2D_BUILD_DIR  "${DEPS_DIR}/blend2d/${BLEND2D_VERSION}/build")
set(BLEND2D_INSTALL    "${DEPS_DIR}/blend2d/${BLEND2D_VERSION}/install")

# 静的ライブラリのビルドオプションを設定
set(BUILD_SHARED_LIBS OFF CACHE BOOL "静的ライブラリをビルド" FORCE)

# ExternalProject ビルド用の並列ビルドジョブ数を決定
if(DEFINED ENV{CMAKE_BUILD_PARALLEL_LEVEL})
  set(PARALLEL_JOBS "$ENV{CMAKE_BUILD_PARALLEL_LEVEL}")
else()
  include(ProcessorCount)
  ProcessorCount(NCORES)
  if(NOT NCORES OR NCORES EQUAL 0)
    set(NCORES 2)
  endif()
  set(PARALLEL_JOBS "${NCORES}")
endif()

# ========== Blend2D ==========
message(STATUS "Setting up Blend2D...")

# Windows では .lib、それ以外では .a
if(WIN32)
  set(BLEND2D_LIB ${BLEND2D_INSTALL}/lib/blend2d.lib)
else()
  set(BLEND2D_LIB ${BLEND2D_INSTALL}/lib/libblend2d.a)
endif()

# ビルド済みかチェック
if(EXISTS ${BLEND2D_LIB})
  message(STATUS "Blend2D already built: ${BLEND2D_LIB}")
  # ダミーターゲットを作成
  add_custom_target(blend2d_ep)
else()
  message(STATUS "Building Blend2D...")
  ExternalProject_Add(blend2d_ep
    URL                 ${BLEND2D_URL}
    URL_HASH            SHA256=${BLEND2D_HASH}
    SOURCE_DIR          ${BLEND2D_SOURCE_DIR}
    BINARY_DIR          ${BLEND2D_BUILD_DIR}
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
    BUILD_COMMAND ${CMAKE_COMMAND} --build <BINARY_DIR> --config Release --parallel ${PARALLEL_JOBS}
    INSTALL_COMMAND ${CMAKE_COMMAND} --build <BINARY_DIR> --config Release --target install
    BUILD_BYPRODUCTS ${BLEND2D_LIB}
  )
endif()

# nanobind モジュール
nanobind_add_module(_blend2d
  NB_DOMAIN "blend2d"
  src/blend2d_ext.cpp
)

# ビルド順序を保証するため依存関係を追加
add_dependencies(_blend2d blend2d_ep)

# インクルードディレクトリ
find_package(Threads)
target_include_directories(_blend2d PRIVATE ${BLEND2D_INSTALL}/include)

# ライブラリをリンク
# Windows では絶対パスを明確に指定
if(WIN32)
  # Windows では文字列として扱って絶対パスを確保
  target_link_libraries(_blend2d PRIVATE
    "${BLEND2D_LIB}"
    Threads::Threads
  )
else()
  # プラットフォーム固有のライブラリ
  if(APPLE)
    target_link_libraries(_blend2d PRIVATE ${BLEND2D_LIB} Threads::Threads)
  elseif(UNIX)
    target_link_libraries(_blend2d PRIVATE ${BLEND2D_LIB} Threads::Threads rt)
  endif()
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
