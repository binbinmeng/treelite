include(FetchContent)

FetchContent_Declare(
  dmlccore
  GIT_REPOSITORY  https://github.com/dmlc/dmlc-core
  GIT_TAG         ff3db4367a30f542aafb83b4af45e685b80102d0
)
FetchContent_MakeAvailable(dmlccore)

FetchContent_Declare(
  fmtlib
  GIT_REPOSITORY  https://github.com/fmtlib/fmt.git
  GIT_TAG         6.2.1
)
FetchContent_MakeAvailable(fmtlib)
set_target_properties(fmt PROPERTIES EXCLUDE_FROM_ALL TRUE)
