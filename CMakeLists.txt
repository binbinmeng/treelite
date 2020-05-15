cmake_minimum_required (VERSION 3.14)
project(treelite LANGUAGES CXX C VERSION 0.9.0)
include(cmake/Utils.cmake)
include(cmake/ExternalLibs.cmake)
include(cmake/Version.cmake)

write_version()

# CMake options
option(USE_OPENMP "Use OpenMP" ON)

# check MSVC version
if(MSVC)
  if(MSVC_VERSION LESS 1910)
    message(FATAL_ERROR "Need Visual Studio 2017 or newer to compile Treelite")
  endif()
endif()

add_subdirectory(src)

# OpenMP
if (USE_OPENMP)
  if (APPLE)
    # Require CMake 3.16+ on Mac OSX, as previous versions of CMake had trouble locating
    # OpenMP on Mac. See https://github.com/dmlc/xgboost/pull/5146#issuecomment-568312706
    cmake_minimum_required(VERSION 3.16)
  endif (APPLE)
  find_package(OpenMP REQUIRED)
  target_link_libraries(objtreelite PUBLIC OpenMP::OpenMP_CXX)
  target_link_libraries(objtreelite_runtime PUBLIC OpenMP::OpenMP_CXX)
else (USE_OPENMP)
  message(STATUS "Disabling OpenMP")
endif (USE_OPENMP)

add_library(treelite SHARED)
target_link_libraries(treelite PUBLIC objtreelite)
add_library(treelite_static STATIC)
target_link_libraries(treelite_static PUBLIC objtreelite)

add_library(treelite_runtime SHARED)
target_link_libraries(treelite_runtime PUBLIC objtreelite_runtime)
add_library(treelite_runtime_static STATIC)
target_link_libraries(treelite_runtime_static PUBLIC objtreelite_runtime)

set_default_configuration_release()
msvc_use_static_runtime()
