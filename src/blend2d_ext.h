#pragma once

#include <blend2d/blend2d.h>

#include <Python.h>
#include <nanobind/nanobind.h>
#include <nanobind/ndarray.h>
#include <nanobind/stl/optional.h>
#include <nanobind/stl/string.h>
#include <cstdint>
#include <string>

namespace nb = nanobind;

struct PyImage {
  BLImage img;
  int width = 0;
  int height = 0;

  PyImage(int w, int h);
  nb::object memoryview();
  nb::object asarray();
};

struct PyPath {
  BLPath path;

  void move_to(double x, double y);
  void line_to(double x, double y);
  void close();
};

struct PyFontFace {
  BLFontFace face;

  PyFontFace();
  void create_from_file(const std::string& filename);
  std::string family_name() const;
  uint32_t weight() const;
};

struct PyFont {
  BLFont font;

  PyFont(PyFontFace& face, float size);
  float size() const;
};

struct DrawContext {
  BLContext ctx;
  bool ended = false;

  DrawContext(PyImage& img);
  ~DrawContext();

  void end();
  void save();
  void restore();
  void set_comp_op(BLCompOp op);
  void set_fill_style_rgba(uint32_t r,
                           uint32_t g,
                           uint32_t b,
                           uint32_t a = 255);
  void translate(double x, double y);
  void rotate(double rad);
  void fill_all();
  void fill_rect(double x, double y, double w, double h);
  void fill_circle(double cx, double cy, double r);
  void fill_pie(double cx, double cy, double r, double start, double sweep);
  void fill_path(PyPath& p);
  void fill_utf8_text(double x, double y, PyFont& font, const std::string& text);
};
