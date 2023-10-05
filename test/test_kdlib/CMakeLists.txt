cmake_minimum_required(VERSION 3.16)
project(test_kdlib)

# C++ Version && C++ Include Directory Settings
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_INCLUDE_CURRENT_DIR ON)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

message("-- System Arch:  ${CMAKE_SYSTEM_PROCESSOR}")
message("-- Current Path: ${CMAKE_SOURCE_DIR}")

if (NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif ()

# executable
add_executable(${PROJECT_NAME} src/main.cpp)

find_package(Qt5 COMPONENTS Core REQUIRED)
find_package(spdlog REQUIRED)
find_package(loggerFactory REQUIRED)
target_link_libraries(${PROJECT_NAME}
        Qt5::Core
        spdlog::spdlog
        KdrobotCppLibs::loggerFactory
        )
