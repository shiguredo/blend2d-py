#include "blend2d_ext.h"

using namespace nb::literals;

// PyImage 実装
PyImage::PyImage(int w, int h) : width(w), height(h) {
  BLResult r = img.create(w, h, BL_FORMAT_PRGB32);
  if (r != BL_SUCCESS) {
    throw std::runtime_error("BLImage.create failed: " + std::to_string(r));
  }
}

nb::object PyImage::memoryview() {
  BLImageData d;
  BLResult r = img.get_data(&d);
  if (r != BL_SUCCESS) {
    throw std::runtime_error("BLImage.get_data failed: " + std::to_string(r));
  }
  Py_ssize_t size = (Py_ssize_t)d.stride * (Py_ssize_t)height;
  PyObject* mv =
      PyMemoryView_FromMemory((char*)d.pixel_data, size, PyBUF_WRITE);
  if (!mv) {
    throw nb::python_error();
  }
  return nb::steal<nb::object>(mv);
}

nb::ndarray<nb::numpy, uint8_t> PyImage::asarray() {
  BLImageData d;
  BLResult r = img.get_data(&d);
  if (r != BL_SUCCESS) {
    throw std::runtime_error("BLImage.get_data failed: " + std::to_string(r));
  }
  // shape: (height, width, 4)
  size_t shape[3] = {(size_t)height, (size_t)width, 4};
  // strides: (stride, 4, 1) バイト単位
  int64_t strides[3] = {(int64_t)d.stride, 4, 1};

  return nb::ndarray<nb::numpy, uint8_t>(d.pixel_data, 3, shape, nb::handle(),
                                         strides);
}

// PyFontFace 実装
PyFontFace::PyFontFace() {}

void PyFontFace::create_from_file(const std::string& filename) {
  BLResult r = face.create_from_file(filename.c_str());
  if (r != BL_SUCCESS) {
    throw std::runtime_error("BLFontFace.create_from_file failed: " +
                             std::to_string(r));
  }
}

std::string PyFontFace::family_name() const {
  return std::string(face.family_name().data(), face.family_name().size());
}

uint32_t PyFontFace::weight() const {
  return face.weight();
}

// PyFont 実装
PyFont::PyFont(PyFontFace& face, float size) {
  BLResult r = font.create_from_face(face.face, size);
  if (r != BL_SUCCESS) {
    throw std::runtime_error("BLFont.create_from_face failed: " +
                             std::to_string(r));
  }
}

float PyFont::size() const {
  return font.size();
}

// PyGradient 実装
PyGradient::PyGradient() {}

void PyGradient::create_linear(double x0, double y0, double x1, double y1, BLExtendMode extend_mode) {
  BLLinearGradientValues values(x0, y0, x1, y1);
  BLResult r = gradient.create(values, extend_mode);
  if (r != BL_SUCCESS) {
    throw std::runtime_error("BLGradient.create (linear) failed: " +
                             std::to_string(r));
  }
}

void PyGradient::create_radial(double x0, double y0, double x1, double y1, double r0, BLExtendMode extend_mode, double r1) {
  BLRadialGradientValues values(x0, y0, x1, y1, r0, r1);
  BLResult r = gradient.create(values, extend_mode);
  if (r != BL_SUCCESS) {
    throw std::runtime_error("BLGradient.create (radial) failed: " +
                             std::to_string(r));
  }
}

void PyGradient::create_conic(double x0, double y0, double angle, BLExtendMode extend_mode, double repeat) {
  BLConicGradientValues values(x0, y0, angle, repeat);
  BLResult r = gradient.create(values, extend_mode);
  if (r != BL_SUCCESS) {
    throw std::runtime_error("BLGradient.create (conic) failed: " +
                             std::to_string(r));
  }
}

void PyGradient::add_stop(double offset, uint32_t r, uint32_t g, uint32_t b, uint32_t a) {
  BLRgba32 color((uint8_t)r, (uint8_t)g, (uint8_t)b, (uint8_t)a);
  BLResult result = gradient.add_stop(offset, color);
  if (result != BL_SUCCESS) {
    throw std::runtime_error("BLGradient.add_stop failed: " +
                             std::to_string(result));
  }
}

void PyGradient::reset_stops() {
  gradient.reset_stops();
}

size_t PyGradient::stop_count() const {
  return gradient.size();
}

BLGradientType PyGradient::gradient_type() const {
  return gradient.type();
}

BLExtendMode PyGradient::extend_mode() const {
  return gradient.extend_mode();
}

// PyPattern 実装
PyPattern::PyPattern() {}

void PyPattern::create(PyImage& image, BLExtendMode extend_mode) {
  BLResult r = pattern.create(image.img, extend_mode);
  if (r != BL_SUCCESS) {
    throw std::runtime_error("BLPattern.create failed: " +
                             std::to_string(r));
  }
}

void PyPattern::set_area(int x, int y, int w, int h) {
  BLRectI area{x, y, w, h};
  BLResult r = pattern.set_area(area);
  if (r != BL_SUCCESS) {
    throw std::runtime_error("BLPattern.set_area failed: " +
                             std::to_string(r));
  }
}

void PyPattern::reset_area() {
  pattern.reset_area();
}

BLExtendMode PyPattern::extend_mode() const {
  return pattern.extend_mode();
}

void PyPattern::set_extend_mode(BLExtendMode extend_mode) {
  BLResult r = pattern.set_extend_mode(extend_mode);
  if (r != BL_SUCCESS) {
    throw std::runtime_error("BLPattern.set_extend_mode failed: " +
                             std::to_string(r));
  }
}

// PyPath 実装
void PyPath::move_to(double x, double y) {
  path.move_to(x, y);
}

void PyPath::line_to(double x, double y) {
  path.line_to(x, y);
}

void PyPath::quad_to(double x1, double y1, double x2, double y2) {
  path.quad_to(x1, y1, x2, y2);
}

void PyPath::cubic_to(double x1, double y1, double x2, double y2, double x3, double y3) {
  path.cubic_to(x1, y1, x2, y2, x3, y3);
}

void PyPath::smooth_quad_to(double x2, double y2) {
  path.smooth_quad_to(x2, y2);
}

void PyPath::smooth_cubic_to(double x2, double y2, double x3, double y3) {
  path.smooth_cubic_to(x2, y2, x3, y3);
}

void PyPath::arc_to(double cx, double cy, double rx, double ry, double start, double sweep, bool force_move_to) {
  path.arc_to(cx, cy, rx, ry, start, sweep, force_move_to);
}

void PyPath::elliptic_arc_to(double rx, double ry, double x_axis_rotation, bool large_arc_flag, bool sweep_flag, double x, double y) {
  path.elliptic_arc_to(rx, ry, x_axis_rotation, large_arc_flag, sweep_flag, x, y);
}

void PyPath::close() {
  path.close();
}

// DrawContext 実装
DrawContext::DrawContext(PyImage& img, uint32_t thread_count) {
  BLContextCreateInfo create_info{};
  create_info.thread_count = thread_count;
  BLResult r = ctx.begin(img.img, create_info);
  if (r != BL_SUCCESS) {
    throw std::runtime_error("BLContext.begin failed: " + std::to_string(r));
  }
}

DrawContext::~DrawContext() {
  if (!ended)
    ctx.end();
}

void DrawContext::end() {
  if (!ended) {
    ctx.end();
    ended = true;
  }
}

void DrawContext::save() {
  ctx.save();
}

void DrawContext::restore() {
  ctx.restore();
}

void DrawContext::set_comp_op(BLCompOp op) {
  ctx.set_comp_op(op);
}

void DrawContext::set_fill_style_rgba(uint32_t r,
                                      uint32_t g,
                                      uint32_t b,
                                      uint32_t a) {
  ctx.set_fill_style(BLRgba32((uint8_t)r, (uint8_t)g, (uint8_t)b, (uint8_t)a));
}

void DrawContext::set_fill_style_gradient(PyGradient& gradient) {
  ctx.set_fill_style(gradient.gradient);
}

void DrawContext::set_fill_style_pattern(PyPattern& pattern) {
  ctx.set_fill_style(pattern.pattern);
}

void DrawContext::set_stroke_style_rgba(uint32_t r,
                                        uint32_t g,
                                        uint32_t b,
                                        uint32_t a) {
  ctx.set_stroke_style(BLRgba32((uint8_t)r, (uint8_t)g, (uint8_t)b, (uint8_t)a));
}

void DrawContext::set_stroke_style_gradient(PyGradient& gradient) {
  ctx.set_stroke_style(gradient.gradient);
}

void DrawContext::set_stroke_style_pattern(PyPattern& pattern) {
  ctx.set_stroke_style(pattern.pattern);
}

void DrawContext::set_stroke_width(double width) {
  ctx.set_stroke_width(width);
}

void DrawContext::set_stroke_miter_limit(double miter_limit) {
  ctx.set_stroke_miter_limit(miter_limit);
}

void DrawContext::set_stroke_join(BLStrokeJoin stroke_join) {
  ctx.set_stroke_join(stroke_join);
}

void DrawContext::set_stroke_caps(BLStrokeCap stroke_cap) {
  ctx.set_stroke_caps(stroke_cap);
}

void DrawContext::translate(double x, double y) {
  ctx.translate(x, y);
}

void DrawContext::rotate(double rad) {
  ctx.rotate(rad);
}

void DrawContext::fill_all() {
  ctx.fill_all();
}

void DrawContext::fill_rect(double x, double y, double w, double h) {
  ctx.fill_rect(BLRect(x, y, w, h));
}

void DrawContext::fill_circle(double cx, double cy, double r) {
  ctx.fill_circle(BLCircle(cx, cy, r));
}

void DrawContext::fill_pie(double cx,
                           double cy,
                           double r,
                           double start,
                           double sweep) {
  ctx.fill_pie(cx, cy, r, start, sweep);
}

void DrawContext::fill_path(PyPath& p) {
  ctx.fill_path(p.path);
}

void DrawContext::fill_utf8_text(double x,
                                  double y,
                                  PyFont& font,
                                  const std::string& text) {
  ctx.fill_utf8_text(BLPoint(x, y), font.font, text.c_str(), text.size());
}

void DrawContext::stroke_rect(double x, double y, double w, double h) {
  ctx.stroke_rect(BLRect(x, y, w, h));
}

void DrawContext::stroke_circle(double cx, double cy, double r) {
  ctx.stroke_circle(BLCircle(cx, cy, r));
}

void DrawContext::stroke_path(PyPath& p) {
  ctx.stroke_path(p.path);
}

// モジュール定義
NB_MODULE(_blend2d, m) {
  m.doc() = "Blend2D bindings (nanobind) with realtime-friendly wrappers";

  // ヘッダの存在確認
  (void)sizeof(BLImage);

  m.def("version",
        []() { return std::string("blend2d-py (nanobind) with Blend2D"); },
        nb::sig("def version() -> str"));

  nb::enum_<BLCompOp>(m, "CompOp")
      .value("SRC_COPY", BL_COMP_OP_SRC_COPY)
      .value("SRC_OVER", BL_COMP_OP_SRC_OVER)
      .export_values();

  nb::enum_<BLExtendMode>(m, "ExtendMode")
      .value("PAD", BL_EXTEND_MODE_PAD)
      .value("REPEAT", BL_EXTEND_MODE_REPEAT)
      .value("REFLECT", BL_EXTEND_MODE_REFLECT)
      .export_values();

  nb::enum_<BLGradientType>(m, "GradientType")
      .value("LINEAR", BL_GRADIENT_TYPE_LINEAR)
      .value("RADIAL", BL_GRADIENT_TYPE_RADIAL)
      .value("CONIC", BL_GRADIENT_TYPE_CONIC)
      .export_values();

  nb::enum_<BLStrokeCap>(m, "StrokeCap")
      .value("BUTT", BL_STROKE_CAP_BUTT)
      .value("SQUARE", BL_STROKE_CAP_SQUARE)
      .value("ROUND", BL_STROKE_CAP_ROUND)
      .value("ROUND_REV", BL_STROKE_CAP_ROUND_REV)
      .value("TRIANGLE", BL_STROKE_CAP_TRIANGLE)
      .value("TRIANGLE_REV", BL_STROKE_CAP_TRIANGLE_REV)
      .export_values();

  nb::enum_<BLStrokeJoin>(m, "StrokeJoin")
      .value("MITER_CLIP", BL_STROKE_JOIN_MITER_CLIP)
      .value("MITER_BEVEL", BL_STROKE_JOIN_MITER_BEVEL)
      .value("MITER_ROUND", BL_STROKE_JOIN_MITER_ROUND)
      .value("BEVEL", BL_STROKE_JOIN_BEVEL)
      .value("ROUND", BL_STROKE_JOIN_ROUND)
      .export_values();

  nb::class_<PyImage>(m, "Image")
      .def(nb::init<int, int>(), "width"_a, "height"_a,
           nb::sig("def __init__(self, width: int, height: int) -> None"))
      .def_prop_ro(
          "width", [](const PyImage& s) { return s.width; },
          nb::sig("def width(self) -> int"))
      .def_prop_ro(
          "height", [](const PyImage& s) { return s.height; },
          nb::sig("def height(self) -> int"))
      .def("memoryview", &PyImage::memoryview,
           nb::sig("def memoryview(self) -> memoryview"),
           "PEP 3118 memoryview (1D, size=stride*height)")
      .def("asarray", &PyImage::asarray,
           "NumPy ndarray view (H, W, 4) uint8; zero-copy");

  nb::class_<PyPath>(m, "Path")
      .def(nb::init<>(), nb::sig("def __init__(self) -> None"))
      .def("move_to", &PyPath::move_to, "x"_a, "y"_a,
           nb::sig("def move_to(self, x: float, y: float) -> None"))
      .def("line_to", &PyPath::line_to, "x"_a, "y"_a,
           nb::sig("def line_to(self, x: float, y: float) -> None"))
      .def("quad_to", &PyPath::quad_to, "x1"_a, "y1"_a, "x2"_a, "y2"_a,
           nb::sig("def quad_to(self, x1: float, y1: float, x2: float, y2: float) -> None"))
      .def("cubic_to", &PyPath::cubic_to, "x1"_a, "y1"_a, "x2"_a, "y2"_a, "x3"_a, "y3"_a,
           nb::sig("def cubic_to(self, x1: float, y1: float, x2: float, y2: float, x3: float, y3: float) -> None"))
      .def("smooth_quad_to", &PyPath::smooth_quad_to, "x2"_a, "y2"_a,
           nb::sig("def smooth_quad_to(self, x2: float, y2: float) -> None"))
      .def("smooth_cubic_to", &PyPath::smooth_cubic_to, "x2"_a, "y2"_a, "x3"_a, "y3"_a,
           nb::sig("def smooth_cubic_to(self, x2: float, y2: float, x3: float, y3: float) -> None"))
      .def("arc_to", &PyPath::arc_to, "cx"_a, "cy"_a, "rx"_a, "ry"_a, "start"_a, "sweep"_a, "force_move_to"_a = false,
           nb::sig("def arc_to(self, cx: float, cy: float, rx: float, ry: float, start: float, sweep: float, force_move_to: bool = False) -> None"))
      .def("elliptic_arc_to", &PyPath::elliptic_arc_to, "rx"_a, "ry"_a, "x_axis_rotation"_a, "large_arc_flag"_a, "sweep_flag"_a, "x"_a, "y"_a,
           nb::sig("def elliptic_arc_to(self, rx: float, ry: float, x_axis_rotation: float, large_arc_flag: bool, sweep_flag: bool, x: float, y: float) -> None"))
      .def("close", &PyPath::close, nb::sig("def close(self) -> None"));

  nb::class_<PyFontFace>(m, "FontFace")
      .def(nb::init<>(), nb::sig("def __init__(self) -> None"))
      .def("create_from_file", &PyFontFace::create_from_file, "filename"_a,
           nb::sig("def create_from_file(self, filename: str) -> None"))
      .def_prop_ro(
          "family_name", [](const PyFontFace& s) { return s.family_name(); },
          nb::sig("def family_name(self) -> str"))
      .def_prop_ro(
          "weight", [](const PyFontFace& s) { return s.weight(); },
          nb::sig("def weight(self) -> int"));

  nb::class_<PyFont>(m, "Font")
      .def(nb::init<PyFontFace&, float>(), "face"_a, "size"_a,
           nb::sig("def __init__(self, face: FontFace, size: float) -> None"))
      .def_prop_ro(
          "size", [](const PyFont& s) { return s.size(); },
          nb::sig("def size(self) -> float"));

  nb::class_<PyGradient>(m, "Gradient")
      .def(nb::init<>(), nb::sig("def __init__(self) -> None"))
      .def("create_linear", &PyGradient::create_linear, "x0"_a, "y0"_a, "x1"_a, "y1"_a, "extend_mode"_a = BL_EXTEND_MODE_PAD,
           nb::sig("def create_linear(self, x0: float, y0: float, x1: float, y1: float, extend_mode: ExtendMode = ExtendMode.PAD) -> None"))
      .def("create_radial", &PyGradient::create_radial, "x0"_a, "y0"_a, "x1"_a, "y1"_a, "r0"_a, "extend_mode"_a = BL_EXTEND_MODE_PAD, "r1"_a = 0.0,
           nb::sig("def create_radial(self, x0: float, y0: float, x1: float, y1: float, r0: float, extend_mode: ExtendMode = ExtendMode.PAD, r1: float = 0.0) -> None"))
      .def("create_conic", &PyGradient::create_conic, "x0"_a, "y0"_a, "angle"_a, "extend_mode"_a = BL_EXTEND_MODE_PAD, "repeat"_a = 1.0,
           nb::sig("def create_conic(self, x0: float, y0: float, angle: float, extend_mode: ExtendMode = ExtendMode.PAD, repeat: float = 1.0) -> None"))
      .def("add_stop", &PyGradient::add_stop, "offset"_a, "r"_a, "g"_a, "b"_a, nb::arg("a") = 255,
           nb::sig("def add_stop(self, offset: float, r: int, g: int, b: int, a: int = 255) -> None"))
      .def("reset_stops", &PyGradient::reset_stops,
           nb::sig("def reset_stops(self) -> None"))
      .def_prop_ro(
          "stop_count", [](const PyGradient& s) { return s.stop_count(); },
          nb::sig("def stop_count(self) -> int"))
      .def_prop_ro(
          "gradient_type", [](const PyGradient& s) { return s.gradient_type(); },
          nb::sig("def gradient_type(self) -> GradientType"))
      .def_prop_ro(
          "extend_mode", [](const PyGradient& s) { return s.extend_mode(); },
          nb::sig("def extend_mode(self) -> ExtendMode"));

  nb::class_<PyPattern>(m, "Pattern")
      .def(nb::init<>(), nb::sig("def __init__(self) -> None"))
      .def("create", &PyPattern::create, "image"_a, "extend_mode"_a = BL_EXTEND_MODE_REPEAT,
           nb::sig("def create(self, image: Image, extend_mode: ExtendMode = ExtendMode.REPEAT) -> None"))
      .def("set_area", &PyPattern::set_area, "x"_a, "y"_a, "w"_a, "h"_a,
           nb::sig("def set_area(self, x: int, y: int, w: int, h: int) -> None"))
      .def("reset_area", &PyPattern::reset_area,
           nb::sig("def reset_area(self) -> None"))
      .def("set_extend_mode", &PyPattern::set_extend_mode, "extend_mode"_a,
           nb::sig("def set_extend_mode(self, extend_mode: ExtendMode) -> None"))
      .def_prop_ro(
          "extend_mode", [](const PyPattern& s) { return s.extend_mode(); },
          nb::sig("def extend_mode(self) -> ExtendMode"));

  nb::class_<DrawContext>(m, "Context")
      .def(nb::init<PyImage&, uint32_t>(), "image"_a, "thread_count"_a = 0,
           nb::sig("def __init__(self, image: Image, thread_count: int = 0) -> None"))
      .def("end", &DrawContext::end, nb::sig("def end(self) -> None"))
      .def("save", &DrawContext::save, nb::sig("def save(self) -> None"))
      .def("restore", &DrawContext::restore,
           nb::sig("def restore(self) -> None"))
      .def("set_comp_op", &DrawContext::set_comp_op, "op"_a,
           nb::sig("def set_comp_op(self, op: CompOp) -> None"))
      .def("set_fill_style_rgba", &DrawContext::set_fill_style_rgba, "r"_a,
           "g"_a, "b"_a, nb::arg("a") = 255,
           nb::sig("def set_fill_style_rgba(self, r: int, g: int, b: int, a: "
                   "int = 255) -> None"))
      .def("set_fill_style_gradient", &DrawContext::set_fill_style_gradient, "gradient"_a,
           nb::sig("def set_fill_style_gradient(self, gradient: Gradient) -> None"))
      .def("set_fill_style_pattern", &DrawContext::set_fill_style_pattern, "pattern"_a,
           nb::sig("def set_fill_style_pattern(self, pattern: Pattern) -> None"))
      .def("set_stroke_style_rgba", &DrawContext::set_stroke_style_rgba, "r"_a,
           "g"_a, "b"_a, nb::arg("a") = 255,
           nb::sig("def set_stroke_style_rgba(self, r: int, g: int, b: int, a: "
                   "int = 255) -> None"))
      .def("set_stroke_style_gradient", &DrawContext::set_stroke_style_gradient, "gradient"_a,
           nb::sig("def set_stroke_style_gradient(self, gradient: Gradient) -> None"))
      .def("set_stroke_style_pattern", &DrawContext::set_stroke_style_pattern, "pattern"_a,
           nb::sig("def set_stroke_style_pattern(self, pattern: Pattern) -> None"))
      .def("set_stroke_width", &DrawContext::set_stroke_width, "width"_a,
           nb::sig("def set_stroke_width(self, width: float) -> None"))
      .def("set_stroke_miter_limit", &DrawContext::set_stroke_miter_limit, "miter_limit"_a,
           nb::sig("def set_stroke_miter_limit(self, miter_limit: float) -> None"))
      .def("set_stroke_join", &DrawContext::set_stroke_join, "stroke_join"_a,
           nb::sig("def set_stroke_join(self, stroke_join: StrokeJoin) -> None"))
      .def("set_stroke_caps", &DrawContext::set_stroke_caps, "stroke_cap"_a,
           nb::sig("def set_stroke_caps(self, stroke_cap: StrokeCap) -> None"))
      .def("translate", &DrawContext::translate, "x"_a, "y"_a,
           nb::sig("def translate(self, x: float, y: float) -> None"))
      .def("rotate", &DrawContext::rotate, "rad"_a,
           nb::sig("def rotate(self, rad: float) -> None"))
      .def("fill_all", &DrawContext::fill_all,
           nb::sig("def fill_all(self) -> None"))
      .def("fill_rect", &DrawContext::fill_rect, "x"_a, "y"_a, "w"_a, "h"_a,
           nb::sig("def fill_rect(self, x: float, y: float, w: float, h: "
                   "float) -> None"))
      .def("fill_circle", &DrawContext::fill_circle, "cx"_a, "cy"_a, "r"_a,
           nb::sig(
               "def fill_circle(self, cx: float, cy: float, r: float) -> None"))
      .def("fill_pie", &DrawContext::fill_pie, "cx"_a, "cy"_a, "r"_a, "start"_a,
           "sweep"_a,
           nb::sig("def fill_pie(self, cx: float, cy: float, r: float, start: "
                   "float, sweep: float) -> None"))
      .def("fill_path", &DrawContext::fill_path, "path"_a,
           nb::sig("def fill_path(self, path: Path) -> None"))
      .def("fill_utf8_text", &DrawContext::fill_utf8_text, "x"_a, "y"_a,
           "font"_a, "text"_a,
           nb::sig("def fill_utf8_text(self, x: float, y: float, font: Font, "
                   "text: str) -> None"))
      .def("stroke_rect", &DrawContext::stroke_rect, "x"_a, "y"_a, "w"_a, "h"_a,
           nb::sig("def stroke_rect(self, x: float, y: float, w: float, h: "
                   "float) -> None"))
      .def("stroke_circle", &DrawContext::stroke_circle, "cx"_a, "cy"_a, "r"_a,
           nb::sig("def stroke_circle(self, cx: float, cy: float, r: float) -> None"))
      .def("stroke_path", &DrawContext::stroke_path, "path"_a,
           nb::sig("def stroke_path(self, path: Path) -> None"))
      .def("__enter__", [](DrawContext& self) -> DrawContext& { return self; })
      .def(
          "__exit__",
          [](DrawContext& self, nb::object, nb::object, nb::object) { self.end(); },
          "exc_type"_a.none(), "exc_val"_a.none(), "exc_tb"_a.none());
}
