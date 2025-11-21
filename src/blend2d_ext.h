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

struct PyGradient {
  BLGradient gradient;

  PyGradient();
  void create_linear(double x0, double y0, double x1, double y1, BLExtendMode extend_mode = BL_EXTEND_MODE_PAD);
  void create_radial(double x0, double y0, double x1, double y1, double r0, BLExtendMode extend_mode = BL_EXTEND_MODE_PAD, double r1 = 0.0);
  void create_conic(double x0, double y0, double angle, BLExtendMode extend_mode = BL_EXTEND_MODE_PAD, double repeat = 1.0);
  void add_stop(double offset, uint32_t r, uint32_t g, uint32_t b, uint32_t a);
  void reset_stops();
  size_t stop_count() const;
  uint32_t gradient_type() const;
  uint32_t extend_mode() const;
};

struct PyPattern {
  BLPattern pattern;

  PyPattern();
  void create(PyImage& image, BLExtendMode extend_mode = BL_EXTEND_MODE_REPEAT);
  void set_area(int x, int y, int w, int h);
  void reset_area();
  uint32_t extend_mode() const;
  void set_extend_mode(BLExtendMode extend_mode);
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
  void set_fill_style_gradient(PyGradient& gradient);
  void set_fill_style_pattern(PyPattern& pattern);
  void set_stroke_style_rgba(uint32_t r,
                              uint32_t g,
                              uint32_t b,
                              uint32_t a = 255);
  void set_stroke_style_gradient(PyGradient& gradient);
  void set_stroke_style_pattern(PyPattern& pattern);
  void set_stroke_width(double width);
  void set_stroke_miter_limit(double miter_limit);
  void set_stroke_join(BLStrokeJoin stroke_join);
  void set_stroke_caps(BLStrokeCap stroke_cap);
  void translate(double x, double y);
  void rotate(double rad);
  void fill_all();
  void fill_rect(double x, double y, double w, double h);
  void fill_circle(double cx, double cy, double r);
  void fill_pie(double cx, double cy, double r, double start, double sweep);
  void fill_path(PyPath& p);
  void fill_utf8_text(double x, double y, PyFont& font, const std::string& text);
  void stroke_rect(double x, double y, double w, double h);
  void stroke_circle(double cx, double cy, double r);
  void stroke_path(PyPath& p);
};
