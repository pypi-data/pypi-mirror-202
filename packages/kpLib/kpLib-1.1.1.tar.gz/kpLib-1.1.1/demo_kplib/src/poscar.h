#ifndef POSCAR_H
#define POSCAR_H

#include <limits>
#include <sstream>
#include <string>
#include <vector>
#include "utils.h"

class Poscar {
public:
  // As read-in from POSCAR.
  Tensor<double> primitiveLattice;

  // Fractional coordinates
  Tensor<double> coordinates;

  // Atom type array with size of the total number of atoms.
  std::vector<int> atomTypes;

  int readFromPoscar(std::string filename);
};

template <class T>
bool from_string(T &t, const std::string &s,
    std::ios_base &(*f)(std::ios_base &)) {
  std::istringstream iss(s);
  return !(iss >> f >> t).fail();
}

#endif // POSCAR_H
