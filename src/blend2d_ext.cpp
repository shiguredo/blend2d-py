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

nb::object PyImage::asarray() {
  // 実装: memoryview -> numpy.frombuffer -> reshape / slice (ゼロコピー)
  nb::object mv = memoryview();
  nb::object np = nb::module_::import_("numpy");
  nb::object uint8 = np.attr("uint8");
  nb::object arr = np.attr("frombuffer")(mv, uint8);
  // (H, -1)
  arr =
      arr.attr("reshape")(nb::make_tuple((Py_ssize_t)height, (Py_ssize_t)-1));
  // [0:H, 0:W*4]
  arr = arr.attr("__getitem__")(nb::make_tuple(
      nb::slice((Py_ssize_t)0, (Py_ssize_t)height, (Py_ssize_t)1),
      nb::slice((Py_ssize_t)0, (Py_ssize_t)width * 4, (Py_ssize_t)1)));
  // (H, W, 4)
  arr = arr.attr("reshape")(
      nb::make_tuple((Py_ssize_t)height, (Py_ssize_t)width, (Py_ssize_t)4));
  return arr;
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

uint32_t PyGradient::gradient_type() const {
  return static_cast<uint32_t>(gradient.type());
}

uint32_t PyGradient::extend_mode() const {
  return static_cast<uint32_t>(gradient.extend_mode());
}

// PyPath 実装
void PyPath::move_to(double x, double y) {
  path.move_to(x, y);
}

void PyPath::line_to(double x, double y) {
  path.line_to(x, y);
}

void PyPath::close() {
  path.close();
}

// DrawContext 実装
DrawContext::DrawContext(PyImage& img) : ctx(img.img) {}

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
           nb::sig("def asarray(self) -> numpy.ndarray[numpy.uint8]"),
           "NumPy ndarray view (H, W, 4) uint8; zero-copy");

  nb::class_<PyPath>(m, "Path")
      .def(nb::init<>(), nb::sig("def __init__(self) -> None"))
      .def("move_to", &PyPath::move_to, "x"_a, "y"_a,
           nb::sig("def move_to(self, x: float, y: float) -> None"))
      .def("line_to", &PyPath::line_to, "x"_a, "y"_a,
           nb::sig("def line_to(self, x: float, y: float) -> None"))
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

  nb::class_<DrawContext>(m, "Context")
      .def(nb::init<PyImage&>(), "image"_a,
           nb::sig("def __init__(self, image: Image) -> None"))
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
                   "text: str) -> None"));
}
