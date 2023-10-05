cd test/test_kdlib && cmake -B build && cmake --build build -j$(nproc) && build/test_kdlib
rm -rf build
