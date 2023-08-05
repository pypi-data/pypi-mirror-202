#include<string>  	// std::stod, std::string,
#include<iostream>
#include<fstream>
#include "precalc.h"

void Precalc::parsePrecalc() {
  std::ifstream ifs(path);
  if (ifs) {
    std::string str;
    while (std::getline(ifs, str)) { // return the ifs object
      parseLine(str);
    }
  } else {
    std::cerr << "Unable to open or read from the PRECALC file: "
        << path << std::endl;
  }
}

void Precalc::parseLine(std::string str) {
  std::size_t found = str.find('=');
  std::string name = str.substr(0, found); // from start to '=';
  std::string value = str.substr(found+1); // from one char after '=' to end.
  if (name == "MINDISTANCE") {
    minDistance = std::stod(value);
  } else if (name == "MINTOTALKPOINTS") {
    minTotalKpoints = std::stoi(value);
  } else if (name == "INCLUDEGAMMA") {
    includeGamma = value;
  } else if (name == "USESCALEFACTOR") {
    useScaleFactor = value;
  }
}

