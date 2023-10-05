cd test/test_opencv && cmake -B build && cmake --build build -j$(nproc) && build/test_opencv
rm -rf build
