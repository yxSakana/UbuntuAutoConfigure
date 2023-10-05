cd test/test_spdlog && cmake -B build && cmake --build build -j$(nproc) && build/test_spdlog
rm -rf build
