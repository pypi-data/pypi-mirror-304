cmake_minimum_required(VERSION 3.18)
set(PROJECT_NAME DSDP)
project(${PROJECT_NAME} LANGUAGES CXX CUDA)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE  ${CMAKE_LIBRARY_OUTPUT_DIRECTORY})
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)

set(CUDA_NVCC_FLAGS -Xcompiler -fopenmp)

install(FILES "src/binding_site_model.pth"
EXCLUDE_FROM_ALL
COMPONENT python_modules
DESTINATION ${PY_BUILD_CMAKE_MODULE_NAME})

install(DIRECTORY "src/test_data"
EXCLUDE_FROM_ALL
COMPONENT python_modules
DESTINATION ${PY_BUILD_CMAKE_MODULE_NAME})

#For protein feature tool
set(FEATURE_SRC "src/protein_feature_tool/protein_feature_tool.cpp")

add_executable(protein_feature_tool ${FEATURE_SRC})

install(FILES "src/protein_feature_tool/17_FEATURES_DATA.txt"
EXCLUDE_FROM_ALL
COMPONENT python_modules
DESTINATION ${PY_BUILD_CMAKE_MODULE_NAME}/protein_feature_tool)

install(TARGETS protein_feature_tool
EXCLUDE_FROM_ALL
COMPONENT python_modules
DESTINATION ${PY_BUILD_CMAKE_MODULE_NAME}/protein_feature_tool)

#For surface tool
set(SURFACE_SRC "src/surface_tool/Surface.cu" "src/surface_tool/common.cu" "src/surface_tool/Run_Surface.cu")
add_executable(surface_tool ${SURFACE_SRC})

install(TARGETS surface_tool
EXCLUDE_FROM_ALL
COMPONENT python_modules
DESTINATION ${PY_BUILD_CMAKE_MODULE_NAME}/surface_tool)

#For blind docking
set(BLIND_SRC "src/DSDP_blind_docking/main_SingleRun.cu" "src/DSDP_blind_docking/common.cu" "src/DSDP_blind_docking/CLUSTER.cu" "src/DSDP_blind_docking/Copy_pdbqt_Format.cu" "src/DSDP_blind_docking/DSDP_Sort.cu" "src/DSDP_blind_docking/DSDP_Task.cu" "src/DSDP_blind_docking/Kernel.cu" "src/DSDP_blind_docking/Neighbor_Grid.cu" "src/DSDP_blind_docking/Partial_Rigid_Small_Molecule.cu" "src/DSDP_blind_docking/Rigid_Protein.cu" "src/DSDP_blind_docking/Vina_Grid_Force_Field.cu" "src/DSDP_blind_docking/Site_Information.cu")
include_directories(${INCLUDES})
add_executable(DSDP_blind ${BLIND_SRC})
install(TARGETS DSDP_blind
EXCLUDE_FROM_ALL
COMPONENT python_modules
DESTINATION ${PY_BUILD_CMAKE_MODULE_NAME}/DSDP_blind_docking)

#For redocking
set(REDOCK_SRC "src/DSDP_redocking/main_SingleRun.cu" "src/DSDP_redocking/common.cu" "src/DSDP_redocking/Copy_pdbqt_Format.cu" "src/DSDP_redocking/DSDP_Sort.cu" "src/DSDP_redocking/DSDP_Task.cu" "src/DSDP_redocking/Kernel.cu" "src/DSDP_redocking/Neighbor_Grid.cu" "src/DSDP_redocking/Partial_Rigid_Small_Molecule.cu" "src/DSDP_redocking/Rigid_Protein.cu" "src/DSDP_redocking/Vina_Grid_Force_Field.cu")
add_executable(DSDP_redock ${REDOCK_SRC})
install(TARGETS DSDP_redock
EXCLUDE_FROM_ALL
COMPONENT python_modules
DESTINATION ${PY_BUILD_CMAKE_MODULE_NAME}/DSDP_redocking)
