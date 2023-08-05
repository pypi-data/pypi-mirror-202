#include "kPointLatticeGenerator.h"
#include "utils.h"
#include "precalc.h"
#include "poscar.h"
#include <iostream>
#include <chrono>

int main(int argc, char **argv) {
  if (argc < 3) {
    std::cerr << "Usage: ./main /path/to/POSCAR /path/to/PRECALC" << std::endl;
    return 1;
  }

  // Parse input files. For demonstration purposes, only POSCAR and PRECALC are needed here.
  Poscar poscar;
  poscar.readFromPoscar(std::string(argv[1]));
  Precalc precalc(argv[2]);

  // Execute the main routines.
  // A wrapper function of the KPointLatticeGenerator constructor, since we need to call spglib to
  // get all arguments for KPointLatticeGenerator constructor.
  KPointLatticeGenerator generator = initializeKPointLatticeGeneratorObject(
      poscar.primitiveLattice, poscar.coordinates, poscar.atomTypes, precalc.getUseScaleFactor());

  if (precalc.getIncludeGamma() == "TRUE") {
    generator.includeGamma(TRUE);
  } else if (precalc.getIncludeGamma() == "FALSE") {
    generator.includeGamma(FALSE);
  } else if (precalc.getIncludeGamma() == "AUTO") {
    generator.includeGamma(AUTO);
  }

  // "auto" is a keyword only defined for c++11.
  //auto start = std::chrono::high_resolution_clock::now();
  KPointLattice lattice =
      generator.getKPointLattice(precalc.getMinDistance(), precalc.getMinTotalKpoints());
  //auto end = std::chrono::high_resolution_clock::now();
  //std::chrono::duration<double> elapsed = end - start;
  //std::cout << "Generate the optimal grid: " << elapsed.count() << " seconds. ";

  if(lattice.getNumDistinctKPoints() == std::numeric_limits<int>::max()) {
    std::cerr << "Error: There is a problem generating k-point grid based on your input. ";
    std::cerr << "If you have activated scale factor, please check your request doesn't exceed ";
    std::cerr << "the maximum allowed number of k-points." << std::endl;
    std::exit(1);
  }
  outputLattice(lattice);
}
