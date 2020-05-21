# Object library

add_library(objtreelite OBJECT)
target_include_directories(objtreelite PUBLIC ${PROJECT_SOURCE_DIR}/include)
target_link_libraries(objtreelite PUBLIC dmlc PRIVATE fmt::fmt-header-only)

add_library(objtreelite_runtime OBJECT)
target_include_directories(objtreelite_runtime PUBLIC ${PROJECT_SOURCE_DIR}/include)
target_link_libraries(objtreelite_runtime PUBLIC dmlc)

set_target_properties(objtreelite objtreelite_runtime
  PROPERTIES
  POSITION_INDEPENDENT_CODE ON
  CXX_STANDARD 11
  CXX_STANDARD_REQUIRED ON)

target_sources(objtreelite
  PRIVATE   c_api/c_api.cc
            c_api/c_api_common.cc
            c_api/c_api_error.cc
            c_api/c_api_error.h
            compiler/ast/ast.h
            compiler/ast/build.cc
            compiler/ast/builder.h
            compiler/ast/dump.cc
            compiler/ast/fold_code.cc
            compiler/ast/is_categorical_array.cc
            compiler/ast/load_data_counts.cc
            compiler/ast/quantize.cc
            compiler/ast/split.cc
            compiler/common/categorical_bitmap.h
            compiler/common/code_folding_util.h
            compiler/common/format_util.h
            compiler/elf/elf_formatter.cc
            compiler/elf/elf_formatter.h
            compiler/native/code_folder_template.h
            compiler/native/header_template.h
            compiler/native/main_template.h
            compiler/native/pred_transform.h
            compiler/native/qnode_template.h
            compiler/ast_native.cc
            compiler/compiler.cc
            compiler/failsafe.cc
            compiler/pred_transform.cc
            compiler/pred_transform.h
            frontend/builder.cc
            frontend/lightgbm.cc
            frontend/xgboost.cc
            annotator.cc
            data.cc
            filesystem.cc
            logging.cc
            optable.cc
            reference_serializer.cc
  PUBLIC    ${PROJECT_SOURCE_DIR}/include/treelite/annotator.h
            ${PROJECT_SOURCE_DIR}/include/treelite/base.h
            ${PROJECT_SOURCE_DIR}/include/treelite/c_api.h
            ${PROJECT_SOURCE_DIR}/include/treelite/c_api_common.h
            ${PROJECT_SOURCE_DIR}/include/treelite/compiler.h
            ${PROJECT_SOURCE_DIR}/include/treelite/compiler_param.h
            ${PROJECT_SOURCE_DIR}/include/treelite/data.h
            ${PROJECT_SOURCE_DIR}/include/treelite/filesystem.h
            ${PROJECT_SOURCE_DIR}/include/treelite/frontend.h
            ${PROJECT_SOURCE_DIR}/include/treelite/logging.h
            ${PROJECT_SOURCE_DIR}/include/treelite/math.h
            ${PROJECT_SOURCE_DIR}/include/treelite/omp.h
            ${PROJECT_SOURCE_DIR}/include/treelite/tree.h
            ${PROJECT_SOURCE_DIR}/include/treelite/tree_impl.h
)

target_sources(objtreelite_runtime
  PRIVATE   c_api/c_api_common.cc
            c_api/c_api_error.cc
            c_api/c_api_error.h
            c_api/c_api_runtime.cc
            predictor/thread_pool/spsc_queue.h
            predictor/thread_pool/thread_pool.h
            predictor/predictor.cc
  PUBLIC    ${PROJECT_SOURCE_DIR}/include/treelite/c_api_common.h
            ${PROJECT_SOURCE_DIR}/include/treelite/c_api_runtime.h
            ${PROJECT_SOURCE_DIR}/include/treelite/entry.h
            ${PROJECT_SOURCE_DIR}/include/treelite/logging.h
            ${PROJECT_SOURCE_DIR}/include/treelite/math.h
            ${PROJECT_SOURCE_DIR}/include/treelite/predictor.h)
