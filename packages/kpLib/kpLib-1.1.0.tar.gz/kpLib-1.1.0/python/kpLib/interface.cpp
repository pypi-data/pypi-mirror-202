#include "kPointLattice.h"
#include "kPointLatticeGenerator.h"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>


namespace py = pybind11;

// The primary binding configuration that wrap both the KPointLattice and
// KPointLatticeGenerator class into python external modules. For reference, see
// the pybind11 doc: https://pybind11.readthedocs.io/en/stable/basics.html.

// First argument: name used in the import statement.
// Second argument: variable identifier used in this block representing this module.
PYBIND11_MODULE(lib, m) {

  m.doc() = "kpLib C++ interface";

  py::enum_<INCLUDE_GAMMA> include_gamma(m, "INCLUDE_GAMMA");
  include_gamma.value("TRUE", INCLUDE_GAMMA::TRUE);
  include_gamma.value("FALSE", INCLUDE_GAMMA::FALSE);
  include_gamma.value("AUTO", INCLUDE_GAMMA::AUTO);

  py::class_<KPointLattice> kpLattice(m, "KPointLattice");
  kpLattice.def("getMinPeriodicDistance", &KPointLattice::getMinPeriodicDistance);
  kpLattice.def("getNumDistinctKPoints", &KPointLattice::getNumDistinctKPoints);
  kpLattice.def("numTotalKPoints", &KPointLattice::numTotalKPoints);

  // The vector<vector<float>> are passed back as list of list in Python.
  kpLattice.def("getKPointCoordinates", &KPointLattice::getKPointCoordinates);
  kpLattice.def("getKPointWeights", &KPointLattice::getKPointWeights);
  //kpLattice.def("getSuperToDirect", &KPointLattice::getSuperToDirect);
  //kpLattice.def("getShift", &KPointLattice::getShift);

  py::class_<KPointLatticeGenerator> kpLatticeGenerator(m, "KPointLatticeGenerator");
  //kpLatticeGenerator.def(py::init<Tensor<double>, Tensor<double>, std::vector<Tensor<int>>, const int, const bool>());
  // Transform the numpy to normal C++ array before using the constructor.
  kpLatticeGenerator.def(py::init(
    [](py::array_t<double, py::array::c_style | py::array::forcecast> npPrimVectors,
       py::array_t<double, py::array::c_style | py::array::forcecast> npConvVectors,
       py::array_t<int, py::array::c_style | py::array::forcecast> npPointOperators,
       const int numOperators,
       const bool isConventionalHexagonal) {
         py::buffer_info info_prim = npPrimVectors.request();
         py::buffer_info info_conv = npConvVectors.request();
         py::buffer_info info_pointOps = npPointOperators.request();
         
         // Multi-dimensional array is a bit different than 1D array. Only passing in the pointer
         // to the first element of the array doesn't work. We should pass in an array of pointers
         // as what a normal 2D C++ array is. So, it's easier to create a C++ 2D array 
         // and copy the numpy values over. 
         double primVectors[3][3];
         double *primPtr = static_cast<double*>(info_prim.ptr);
         for (int r = 0; r < 3; r++) {
            for (int c = 0; c < 3; c++) {
                primVectors[r][c] = primPtr[r * 3 + c];
            }
         }

         // Transfer the conventional lattice vectors
         double convVectors[3][3];
         double *convPtr = static_cast<double*>(info_conv.ptr);
         for (int r = 0; r < 3; r++) {
            for (int c = 0; c < 3; c++) {
                convVectors[r][c] = convPtr[r * 3 + c];
            }
         }

         // Transfer the point operators
         int pointOps[info_pointOps.shape[0]][3][3];
         int *pointOpsPtr = static_cast<int*>(info_pointOps.ptr);
         for (int r = 0; r < info_pointOps.shape[0]; r++) {
            for (int i = 0; i < 3; i++) {
                for (int j = 0; j < 3; j++) {
                    pointOps[r][i][j] = pointOpsPtr[r * 9 + i * 3 + j];
                }
            }
         }
         // The pointers are copied and pass-by-value. The values are not copied.
         return new KPointLatticeGenerator(primVectors, convVectors, pointOps, numOperators,
                                           isConventionalHexagonal);
       }
  ));
  kpLatticeGenerator.def("getKPointLattice", (KPointLattice(KPointLatticeGenerator::*)(const double, const int)) &KPointLatticeGenerator::getKPointLattice);
  kpLatticeGenerator.def("includeGamma", &KPointLatticeGenerator::includeGamma);
  kpLatticeGenerator.def("useScaleFactor", &KPointLatticeGenerator::useScaleFactor);
}
