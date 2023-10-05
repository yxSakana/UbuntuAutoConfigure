cd test/test_qt && cmake -B build && cmake --build build -j$(nproc) && build/test_qt
rm -rf build
