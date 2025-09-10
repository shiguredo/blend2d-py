#include <blend2d.h>

#include <Python.h>
#include <nanobind/nanobind.h>
#include <nanobind/ndarray.h>
#include <nanobind/stl/optional.h>
#include <nanobind/stl/string.h>
#include <cstdint>
#include <string>

namespace nb = nanobind;
using namespace nb::literals;

struct PyImage {
  BLImage img;
  int width = 0;
  int height = 0;

  PyImage(int w, int h) : width(w), height(h) {
    BLResult r = img.create(w, h, BL_FORMAT_PRGB32);
    if (r != BL_SUCCESS) {
      throw std::runtime_error("BLImage.create failed: " + std::to_string(r));
    }
  }

  nb::object memoryview() {
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

  nb::object asarray() {
    // 実装: memoryview -> numpy.frombuffer -> reshape / slice（ゼロコピー）
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
};

struct PyPath {
  BLPath path;

  void move_to(double x, double y) { path.move_to(x, y); }
  void line_to(double x, double y) { path.line_to(x, y); }
  void close() { path.close(); }
};

struct DrawContext {
  BLContext ctx;
  bool ended = false;

  DrawContext(PyImage& img) : ctx(img.img) {}
  ~DrawContext() {
    if (!ended)
      ctx.end();
  }

  void end() {
    if (!ended) {
      ctx.end();
      ended = true;
    }
  }
  void save() { ctx.save(); }
  void restore() { ctx.restore(); }
  void set_comp_op(BLCompOp op) { ctx.set_comp_op(op); }

  void set_fill_style_rgba(uint32_t r,
                           uint32_t g,
                           uint32_t b,
                           uint32_t a = 255) {
    ctx.set_fill_style(
        BLRgba32((uint8_t)r, (uint8_t)g, (uint8_t)b, (uint8_t)a));
  }
  void translate(double x, double y) { ctx.translate(x, y); }
  void rotate(double rad) { ctx.rotate(rad); }
  void fill_all() { ctx.fill_all(); }
  void fill_rect(double x, double y, double w, double h) {
    ctx.fill_rect(BLRect(x, y, w, h));
  }
  void fill_circle(double cx, double cy, double r) {
    ctx.fill_circle(BLCircle(cx, cy, r));
  }
  void fill_pie(double cx, double cy, double r, double start, double sweep) {
    ctx.fill_pie(cx, cy, r, start, sweep);
  }
  void fill_path(PyPath& p) { ctx.fill_path(p.path); }
};

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
           nb::sig("def fill_path(self, path: Path) -> None"));
}
