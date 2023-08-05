cmake_minimum_required(VERSION 2.6)
project(demo_kplib)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -Wall -Werror -fPIC")
set(CMAKE_CXX_FLAGS_DEBUG "-O0 -g")                 # Debug mode.
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -march=native")    # Default optimization.

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif(NOT CMAKE_BUILD_TYPE)

if(CMAKE_BUILD_TYPE MATCHES DEBUG)
    set(CMAKE_EXE_LINKER_FLAGS "-L /usr/local/lib ${CMAKE_EXE_LINKER_FLAGS} -Wl,--no-as-needed -lprofiler -Wl,--as-needed")
endif(CMAKE_BUILD_TYPE MATCHES DEBUG)

find_library(KPLIB kpoints PATHS ../build)
find_library(SPGLIB symspg PATHS ${CMAKE_CURRENT_SOURCE_DIR}/lib /usr/lib /usr/local/lib)

# parent scope variable is inherited. Use a different name here.
set(SOURCES_DEMO ${CMAKE_CURRENT_SOURCE_DIR}/src/utils.cpp
                 ${CMAKE_CURRENT_SOURCE_DIR}/src/poscar.cpp
                 ${CMAKE_CURRENT_SOURCE_DIR}/src/precalc.cpp
                 ${CMAKE_CURRENT_SOURCE_DIR}/src/main.cpp)

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include ../src)

add_executable(demo_kplib ${SOURCES_DEMO})
target_link_libraries(demo_kplib ${KPLIB} ${SPGLIB})
