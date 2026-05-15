cmake_minimum_required(VERSION 3.8)
project(rover_agricola_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Encontrar dependencias
find_package(ament_cmake REQUIRED)

# Instalar los directorios de configuración y modelos
install(
  DIRECTORY
    launch
    urdf
    config
    maps
    rviz
  DESTINATION share/${PROJECT_NAME}
)

ament_package()