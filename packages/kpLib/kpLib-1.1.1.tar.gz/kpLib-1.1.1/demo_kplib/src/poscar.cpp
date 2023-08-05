#include <algorithm>
#include <fstream>
#include <iostream>
#include <sstream>

#include "poscar.h"

int Poscar::readFromPoscar(std::string filename) {
  std::vector<std::string> textStream;
  std::string line;
  std::ifstream fileInputStream;
  int idx, i = 0, j = 0;
  bool cart;
  double xx;

  primitiveLattice = Tensor<double>(3, std::vector<double>(3, 0));
  coordinates = Tensor<double>();
  atomTypes = std::vector<int>();

  fileInputStream.open(filename.c_str(), std::ios::in);

  if (fileInputStream.is_open()) {
    while (!fileInputStream.eof()) {
      getline(fileInputStream, line);
      textStream.push_back(line);
    }
    fileInputStream.close();
  } else {
    std::cerr << "Unable to open file." << std::endl;
    return 0;
  }

  // Reading lattice vectors
  i = 0;
  for (idx = 2; idx < 5; idx++) {
    j = 0;
    std::stringstream iss(textStream[idx]);
    std::string buf;
    while (iss >> buf) {
      if (from_string<double>(xx, std::string(buf), std::dec)) {
        primitiveLattice[i][j] = xx * std::atof(textStream[1].c_str());
        j++;
      }
    }
    i++;
  }

  // Reading atom type counts
  std::stringstream iss(textStream[6]);
  std::string buf;
  int currType = 1, num = 0, totalNum = 0;
  while (iss >> buf) {
    if (from_string<int>(num, std::string(buf), std::dec)) {
      totalNum += num;
      atomTypes.resize((size_t) totalNum, currType);
      currType++;
    }
  }

  // Checking whether the coordinates are in Cartesian or Direct form
  if (textStream[7].at(0) == 'K' || textStream[7].at(0) == 'k' ||
      textStream[7].at(0) == 'C' || textStream[7].at(0) == 'c') {
    cart = true;
  } else {
    cart = false;
  }

  // Reading atom coordinates
  coordinates.resize(atomTypes.size());
  i = 0;
  for (idx = 8; idx < (int) textStream.size(); idx++) {
    std::stringstream iss(textStream[idx]);
    std::string buf;
    std::vector<double> currCoord = std::vector<double>(3, 0.0);
    j = 0;
    while (iss >> buf) {
      if (from_string<double>(xx, std::string(buf), std::dec)) {
        currCoord[j] = xx;
        j++;
      }
    }

    // Doesn't consider selective dynamics.
    if (j == 3) { // not a valid coordinate.
      if (cart) {
        // spglib uses exclusively fractional coordinates.
        coordinates[i] = matrixTimesVector(simpleInverse(primitiveLattice), currCoord);
      } else {
        coordinates[i] = currCoord;
      }
      i++;
    } else {
      break; // blank line.
    }
  }
  return 1;
}
