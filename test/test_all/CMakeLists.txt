cmake_minimum_required(VERSION 3.16)
project(test)

# C++ Version && C++ Include Directory Settings
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_INCLUDE_CURRENT_DIR ON)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# QT Settings
set(IS_DEPEND_QT ON)
set(QT_VERSION 5)

if (IS_DEPEND_QT STREQUAL "ON")
    set(CMAKE_AUTOUIC ON)
    set(CMAKE_AUTOMOC ON)
    set(CMAKE_AUTORCC ON)
endif ()

message("-- System Arch:  ${CMAKE_SYSTEM_PROCESSOR}")
message("-- Current Path: ${CMAKE_SOURCE_DIR}")

if (NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif ()


# sources file
file(GLOB_RECURSE sources CONFIGURE_DEPENDS src/*.cpp src/*.h)
# executable
add_executable(${PROJECT_NAME} ${sources})

# include directory
set(IncludeDirectory
        )
# package
set(DEPEND_PACKAGES
        Threads
        spdlog
        realsense2
        OpenCV
        Eigen3
        loggerFactory
        )
set(QT_PACKAGES
        Core
        Widgets
        )
# library
set(DEPEND_LIBRARIES
        Threads::Threads
        spdlog::spdlog
        realsense2
        Eigen3::Eigen
        KdrobotCppLibs::loggerFactory
        )


target_include_directories(${PROJECT_NAME} PUBLIC ${IncludeDirectory})

foreach (PACKAGE ${DEPEND_PACKAGES})
    find_package(${PACKAGE} REQUIRED)
endforeach ()
if (IS_DEPEND_QT STREQUAL "ON")
    foreach (QT_PACKAGE ${QT_PACKAGES})
        find_package(Qt${QT_VERSION} COMPONENTS ${QT_PACKAGE} REQUIRED)
    endforeach ()
endif ()

foreach (LIBRARY ${DEPEND_LIBRARIES})
    target_link_libraries(${PROJECT_NAME} ${LIBRARY})
endforeach ()
if (IS_DEPEND_QT STREQUAL "ON")
    foreach (QT_PACKAGE ${QT_PACKAGES})
        target_link_libraries(${PROJECT_NAME} Qt${QT_VERSION}::${QT_PACKAGE})
    endforeach ()
endif ()
target_link_libraries(${PROJECT_NAME} ${OpenCV_LIBS})
