#ifndef PRECALC_H_
#define PRECALC_H_

#include <string>

class Precalc {
  const char* path; // a c-string for ifstream;
  // default values;
  double minDistance = 0.1;
  int minTotalKpoints = 1;
  std::string includeGamma = "AUTO";
  std::string useScaleFactor = "FALSE";

public:
  Precalc(const char* str) {
    path = str;
    parsePrecalc();
  }

  double getMinDistance() { return minDistance; }
  int getMinTotalKpoints() { return minTotalKpoints; }
  std::string getIncludeGamma() { return includeGamma; }
  std::string getUseScaleFactor() { return useScaleFactor; }

private:
  void parsePrecalc();
  void parseLine(std::string);
};

#endif /* PRECALC_H_ */
