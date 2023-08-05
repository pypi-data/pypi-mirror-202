#include "utils.h"
#include "spglib.h"
#include <iomanip>
#include <iostream>
#include <algorithm>

KPointLatticeGenerator initializeKPointLatticeGeneratorObject(Tensor<double> &primitiveLattice,
    Tensor<double> &coordinates, std::vector<int> &atomTypes, std::string useScaleFactor ) {

  double conventionalLatticeArray[3][3] = {0};
  double primLatticeArray[3][3] = {0};
  double coordinatesArray[coordinates.size()][3];
  for (int i = 0; i < (int) coordinates.size(); i++) {
    coordinatesArray[i][0] = 0;
    coordinatesArray[i][1] = 0;
    coordinatesArray[i][2] = 0;
  }
  int atomTypesArray[atomTypes.size()];
  for (int i = 0; i < (int) atomTypes.size(); i++) {
    atomTypesArray[i] = 0;
  }

  int num_atom = coordinates.size();
  int size;
  int rotation[max_size][3][3] = {0};
  double translation[max_size][3] = {0};
  bool isConventionalHexagonal = false;

  // spglib uses column vectors convention.
  // Pad the former with the latter.
  vectorToArr(primLatticeArray, primitiveLattice);
  transpose(primLatticeArray);	// transpose to spglib convention;
  vectorToArr(conventionalLatticeArray, primitiveLattice);
  transpose(conventionalLatticeArray); // transpose to spglib convention;
  vectorToArr(coordinatesArray, coordinates);
  vectorToArr(atomTypesArray, atomTypes);

  size = spg_get_symmetry(rotation, translation, max_size, primLatticeArray, coordinatesArray,
      atomTypesArray, num_atom, symprec);

  // Since standardization could expand the array up to 4 times
  // in face-centered case.
  double conventionalCoordArray[coordinates.size() * 4][3];
  for (int i = 0; i < (int) coordinates.size() * 4; i++) {
    conventionalCoordArray[i][0] = 0;
    conventionalCoordArray[i][1] = 0;
    conventionalCoordArray[i][2] = 0;
  }
  int conventionalTypeArray[atomTypes.size() * 4];
  for (int i = 0; i < (int) atomTypes.size() * 4; i++) {
    conventionalTypeArray[i] = 0;
  }
  vectorToArr(conventionalCoordArray, coordinates);
  vectorToArr(conventionalTypeArray, atomTypes);

  // to_primitive = 0: return a standard conventional lattice.
  // no_idealization = 1: don't rotate the crystal to idealize the lattice. See spglib manual.
  spg_standardize_cell(conventionalLatticeArray, conventionalCoordArray, conventionalTypeArray,
      num_atom, 0, 1, symprec);

  SpglibDataset * dataSet = spg_get_dataset(primLatticeArray, coordinatesArray,
      atomTypesArray, num_atom, symprec);

  int spaceGroup = dataSet->spacegroup_number;
  // The monoclinic system (2/m Laue class) should use the 2-fold axis
  // as the 3rd-vector in the conventional lattice.
  if (spaceGroup >=3 && spaceGroup <= 15) {
    // Make the e_pri direction in spglib the 3rd vector.
    // We do this by swapping the column vectors: 1->2; 2->3; 3->1, to keep determinant positive.
    double temp;
    for (int i = 0; i < 3; i++) { // row
      temp = conventionalLatticeArray[i][2];
      conventionalLatticeArray[i][2] = conventionalLatticeArray[i][1];
      conventionalLatticeArray[i][1] = conventionalLatticeArray[i][0];
      conventionalLatticeArray[i][0] = temp;
    }
  } else if (spaceGroup >= 143 && spaceGroup <= 194) {
    // For trigonal systems, we always use the hP lattice setting. I.e. conventional lattice
    // of a trigonal lattice is always a hexagonal lattice. It is a bit different from the
    // international standard defined in "ITA: International Tables for Crystallography, Volume A."
    // But the original input lattice vectors won't be modified 
    // and the rotational operations are still in the basis of the input lattice vectors.
    
    isConventionalHexagonal = true;
  }

  // Add inversion if the structure doesn't have one, since reciprocal space
  // always have inversion if not explicitly removed.
  adjustOperators(rotation, size, "none");

  // Take transpose of rotation to follow convention used in kplib.
  transpose(conventionalLatticeArray);
  transpose(primLatticeArray);
  for (int n = 0; n < size; n++) {
    int temp = 0;
    for (int i = 1; i < 3; i++) {
      for (int j = 0; j < i; j++) {
        temp = rotation[n][j][i];
        rotation[n][j][i] = rotation[n][i][j];
        rotation[n][i][j] = temp;
      }
    }
  }

  // Initialize the generator.
  // The kplib convention:
  //    1. Lattice vectors as rows: 				A = (a, b, c)^T
  //    2. Symmetry operation on fractional coords: x' = x*R
  //    3. Lattice Transformation: 					A' = M*A
  KPointLatticeGenerator generator = KPointLatticeGenerator(primLatticeArray,
      conventionalLatticeArray, rotation, size, isConventionalHexagonal);

  if (useScaleFactor == "TRUE") {
    generator.useScaleFactor(spaceGroup); // Otherwise, use the fully dynamic search.
  }

  return generator;
}

/*
 * Adjust the point group to that of the corresponding Laue Class.
 *
 * @param removedSymmetry	"NONE"/"ALL"/"STRUCTURAL"/"TIME_REVERSAL"
 */
void adjustOperators(int rotation[][3][3], int& size, std::string removedSymmetry) {

  std::transform(removedSymmetry.begin(), removedSymmetry.end(),
      removedSymmetry.begin(), [](unsigned char c) { return std::toupper(c); });
  bool hasInversion = false;

  // We use spglib as a demo. Users of the library should decide what
  // symmetries they want to remove.
  if (removedSymmetry == "NONE") {
    // Add inversion to the group;
    for (int i = 0; i < size; i++) {
      int trace = rotation[i][0][0] + rotation[i][1][1] + rotation[i][2][2];
      if (trace == -3) {
        hasInversion = true;
        break;
      }
    }
    if (!hasInversion) { // Add inversion if the structure doesn't have it --> make it Laue class.
      int originalSize = size;
      size *= 2;
      for (int n = 0; n < originalSize; n++) {
        for (int i = 0; i < 3; i++) {
          for (int j = 0; j < 3; j++) {
            rotation[originalSize + n][i][j] = -1 * rotation[n][i][j];
          }
        }
      }
    }
  }
}

void outputLattice(KPointLattice &lattice) {
  Tensor<int> superToDirect = lattice.getSuperToDirect();
  double actualPeriodicDistance = lattice.getMinPeriodicDistance();
  int distinctKpts = lattice.getNumDistinctKPoints();
  Tensor<double> coords = lattice.getKPointCoordinates();
  std::vector<int> weights = lattice.getKPointWeights();


  // Output for debugging.
  /*
  std::cout << "Super to direct matrix: " << std::endl;
  std::cout << superToDirect[0][0] << " " << superToDirect[0][1] << " "
            << superToDirect[0][2] << std::endl;
  std::cout << superToDirect[1][0] << " " << superToDirect[1][1] << " "
            << superToDirect[1][2] << std::endl;
  std::cout << superToDirect[2][0] << " " << superToDirect[2][1] << " "
            << superToDirect[2][2] << std::endl;
  std::vector<double> shiftVec = lattice.getShift();
  std::cout << shiftVec[0] << " " << shiftVec[1] << " " << shiftVec[2] << std::endl;
  */

  // Output to KPOINTS
  std::cout << "K-point grid has " << coords.size() << " total points. ";
  std::cout << "Actual minimum periodic distance is " << std::fixed << std::setprecision(15)
  << actualPeriodicDistance << " Angstroms." << std::endl;
  std::cout << distinctKpts << std:: endl;
  std::cout << "Fractional" << std::endl;
  int distIndex = 0;
  for (int i = 0; i < (int) coords.size(); ++i) {
    // Only k-points with weights larger than 0 are distinct ones.
    if (weights[i] > 0) {
      distIndex++;
      std::cout << std::setprecision(14) << coords[i][0]
                << " " << std::setprecision(14) << coords[i][1]
                << " " << std::setprecision(14) << coords[i][2]
                << " " << std::setprecision(1)  << (double) weights[i]
                << " ! " << distIndex << std::endl;
    }
  }
}

//---------------------------------- Utility functions -------------------------------------------//
/*
 * Fast and simple implementation of 3x3 matrix manipulations.
 */
template<class T>
void transpose(T matrix[][3]) {
  double temp = 0;
  for (int i = 1; i < 3; i++) {
    for (int j = 0; j < i; j++) {
      temp = matrix[j][i];
      matrix[j][i] = matrix[i][j];
      matrix[i][j] = temp;
    }
  }
}

/*
 * Simple 3x3 matrix inverse.
 */
void simpleInverse(double matrix[][3]) {
  double inverseMatrix[3][3];

  double det = matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
    		                       - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
    		                       + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0]);

  inverseMatrix[0][0] = (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1]) / det;
  inverseMatrix[0][1] = (matrix[0][2] * matrix[2][1] - matrix[2][2] * matrix[0][1]) / det;
  inverseMatrix[0][2] = (matrix[0][1] * matrix[1][2] - matrix[0][2] * matrix[1][1]) / det;
  inverseMatrix[1][0] = (matrix[1][2] * matrix[2][0] - matrix[1][0] * matrix[2][2]) / det;
  inverseMatrix[1][1] = (matrix[0][0] * matrix[2][2] - matrix[0][2] * matrix[2][0]) / det;
  inverseMatrix[1][2] = (matrix[1][0] * matrix[0][2] - matrix[1][2] * matrix[0][0]) / det;
  inverseMatrix[2][0] = (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0]) / det;
  inverseMatrix[2][1] = (matrix[0][1] * matrix[2][0] - matrix[0][0] * matrix[2][1]) / det;
  inverseMatrix[2][2] = (matrix[1][1] * matrix[0][0] - matrix[1][0] * matrix[0][1]) / det;

  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
      matrix[i][j] = inverseMatrix[i][j];
    }
  }
}

Tensor<double> simpleInverse(const Tensor<double> &matrix) {

  Tensor<double> inverseMatrix(3, std::vector<double>(3, 0));
  double det = matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
    		                       - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
    		                       + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0]);

  inverseMatrix[0][0] = (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1]) / det;
  inverseMatrix[0][1] = (matrix[0][2] * matrix[2][1] - matrix[2][2] * matrix[0][1]) / det;
  inverseMatrix[0][2] = (matrix[0][1] * matrix[1][2] - matrix[0][2] * matrix[1][1]) / det;
  inverseMatrix[1][0] = (matrix[1][2] * matrix[2][0] - matrix[1][0] * matrix[2][2]) / det;
  inverseMatrix[1][1] = (matrix[0][0] * matrix[2][2] - matrix[0][2] * matrix[2][0]) / det;
  inverseMatrix[1][2] = (matrix[1][0] * matrix[0][2] - matrix[1][2] * matrix[0][0]) / det;
  inverseMatrix[2][0] = (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0]) / det;
  inverseMatrix[2][1] = (matrix[0][1] * matrix[2][0] - matrix[0][0] * matrix[2][1]) / det;
  inverseMatrix[2][2] = (matrix[1][1] * matrix[0][0] - matrix[1][0] * matrix[0][1]) / det;

  return inverseMatrix;

}

std::vector<double> matrixTimesVector(const Tensor<double> &matrix, const std::vector<double> &vec) {

  if ((int) matrix.size() == 0) {
    return std::vector<double>();
  }

  std::vector<double> result(matrix.size(), 0);

  for (int rowNum = 0; rowNum < (int)  matrix.size(); rowNum++) {
    //std::vector<double> row = matrix[rowNum];
    result[rowNum] = matrix[rowNum][0] * vec[0] + matrix[rowNum][1] * vec[1]
                                                                          + matrix[rowNum][2] * vec[2];
  }

  return result;
}

void vectorToArr(double temp[][3], const Tensor<double> &vals) {
  for (int i = 0; (i < (int) vals.size()); i++) {
    for (int j = 0; (j < (int) vals[0].size()); j++) {
      temp[i][j] = vals[i][j];
    }
  }
}

void vectorToArr(int temp[], const std::vector<int> &vals) {
  for (int i = 0; (i < (int) vals.size()); i++) {
    temp[i] = vals[i];
  }
}

void arrToVec(Tensor<double> &vals, const double temp[][3], const int N, const int M) {
  for (int i = 0; (i < N); i++) {
    for (int j = 0; (j < M); j++) {
      vals[i][j] = temp[i][j];
    }
  }
}

void arrToVec(std::vector<Tensor<int> > &vals, const int temp[][3][3], const int N,
    const int M, const int P) {
  for (int i = 0; (i < N); i++) {
    for (int j = 0; (j < M); j++) {
      for (int k = 0; (k < P); k++) {
        vals[i][j][k] = temp[i][j][k];
      }
    }
  }
}
