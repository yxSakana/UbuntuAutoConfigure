cd test/test_realsense2 && cmake -B build && cmake --build build -j$(nproc) && build/test_realsense2
rm -rf build
