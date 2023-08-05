#ifndef UTILS_H
#define UTILS_H

#include "kPointLatticeGenerator.h"

// Precision for deciding whether two coordinates are coincidental.
static const double symprec = 1e-5;

// Max number of sym ops allowed. See spglib.c:line 1504.
static const int max_size = 192; // 48 * 4.

KPointLatticeGenerator initializeKPointLatticeGeneratorObject(Tensor<double> &primitiveLattice,
    Tensor<double> &coordinates, std::vector<int> &atomTypes, std::string useScaleFactor);

void adjustOperators(int rotation[][3][3], int& size, std::string removedSymmetry);
void outputLattice(KPointLattice &lattice);

// Utility functions.
// Most of them are duplicate ones in the MSMath.h. They are redefined to minimize the dependency
// on the kplib library. Most of DFT packages have their own implementations of these anyway.
template<class T> void transpose(T matrix[][3]);
void simpleInverse(double matrix[][3]);

std::vector<double> matrixTimesVector(const Tensor<double> &matrix, const std::vector<double> &vec);
Tensor<double> simpleInverse(const Tensor<double> &matrix);

void vectorToArr(double temp[][3], const Tensor<double> &vals);
void vectorToArr(int temp[], const std::vector<int> &vals);
void arrToVec(Tensor<double> &vals, const double temp[][3], const int N, const int M);
void arrToVec(std::vector<Tensor<int> > &vals, const int temp[][3][3], const int N, const int M, const int P);

#endif // UTILS_H
