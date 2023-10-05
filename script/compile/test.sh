cd test/test_all && cmake -B build && cmake --build build -j$(nproc) && build/test
rm -rf build
