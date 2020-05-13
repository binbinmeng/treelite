cmake_minimum_required (VERSION 3.14)
project(treelite)
include(cmake/Utils.cmake)
include(cmake/ExternalLibs.cmake)

# CMake options
option(USE_OPENMP "Use OpenMP" ON)

# check MSVC version
if(MSVC)
  if(MSVC_VERSION LESS 1910)
    message(FATAL_ERROR "Need Visual Studio 2017 or newer to compile Treelite")
  endif()
endif()

set(SOURCES
  include/treelite/annotator.h
  include/treelite/base.h
  include/treelite/c_api.h
  include/treelite/c_api_common.h
  include/treelite/compiler.h
  include/treelite/compiler_param.h
  include/treelite/data.h
  include/treelite/filesystem.h
  include/treelite/frontend.h
  include/treelite/logging.h
  include/treelite/math.h
  include/treelite/omp.h
  include/treelite/tree.h
  include/treelite/tree_impl.h
  src/c_api/c_api.cc
  src/c_api/c_api_common.cc
  src/c_api/c_api_error.cc
  src/c_api/c_api_error.h
  src/compiler/ast/ast.h
  src/compiler/ast/build.cc
  src/compiler/ast/builder.h
  src/compiler/ast/dump.cc
  src/compiler/ast/fold_code.cc
  src/compiler/ast/is_categorical_array.cc
  src/compiler/ast/load_data_counts.cc
  src/compiler/ast/quantize.cc
  src/compiler/ast/split.cc
  src/compiler/common/categorical_bitmap.h
  src/compiler/common/code_folding_util.h
  src/compiler/common/format_util.h
  src/compiler/elf/elf_formatter.cc
  src/compiler/elf/elf_formatter.h
  src/compiler/native/code_folder_template.h
  src/compiler/native/header_template.h
  src/compiler/native/main_template.h
  src/compiler/native/pred_transform.h
  src/compiler/native/qnode_template.h
  src/compiler/ast_native.cc
  src/compiler/compiler.cc
  src/compiler/failsafe.cc
  src/compiler/pred_transform.cc
  src/compiler/pred_transform.h
  src/frontend/builder.cc
  src/frontend/lightgbm.cc
  src/frontend/model.cc
  src/frontend/xgboost.cc
  src/annotator.cc
  src/data.cc
  src/filesystem.cc
  src/logging.cc
  src/optable.cc
  src/reference_serializer.cc
)

set(RUNTIME_SOURCES
  include/treelite/c_api_common.h
  include/treelite/c_api_runtime.h
  include/treelite/entry.h
  include/treelite/logging.h
  include/treelite/math.h
  include/treelite/predictor.h
  src/c_api/c_api_common.cc
  src/c_api/c_api_error.cc
  src/c_api/c_api_error.h
  src/c_api/c_api_runtime.cc
  src/predictor/thread_pool/spsc_queue.h
  src/predictor/thread_pool/thread_pool.h
  src/predictor/predictor.cc
)

add_library(objtreelite OBJECT ${SOURCES})
target_include_directories(objtreelite PUBLIC include)
target_link_libraries(objtreelite PUBLIC dmlc PRIVATE fmt::fmt)

add_library(objtreelite_runtime OBJECT ${RUNTIME_SOURCES})
target_include_directories(objtreelite_runtime PUBLIC include)
target_link_libraries(objtreelite_runtime PUBLIC dmlc)

# OpenMP
if (USE_OPENMP)
  if (APPLE)
    # Require CMake 3.16+ on Mac OSX, as previous versions of CMake had trouble locating
    # OpenMP on Mac. See https://github.com/dmlc/xgboost/pull/5146#issuecomment-568312706
    cmake_minimum_required(VERSION 3.16)
  endif (APPLE)
  find_package(OpenMP REQUIRED)
  target_link_libraries(objtreelite PUBLIC OpenMP::OpenMP_CXX)
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

set_target_properties(objtreelite objtreelite_runtime fmt
  PROPERTIES
  POSITION_INDEPENDENT_CODE ON
  CXX_STANDARD 11
  CXX_STANDARD_REQUIRED ON)

set_default_configuration_release()
msvc_use_static_runtime()
