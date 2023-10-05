/**
 * @projectName test
 * @file main.cpp
 * @brief 
 * 
 * @author yx 
 * @date 2023-10-05 22:11
 */

#include <iostream>
#include <librealsense2/rs.hpp>

int main() {
    // 初始化RealSense库
    rs2::context ctx;
    if (ctx.query_devices().size() == 0) {
        std::cerr << "No RealSense devices detected!" << std::endl;
        return EXIT_FAILURE;
    }

    // 获取第一个连接的RealSense设备
    rs2::device dev = ctx.query_devices().front();

    // 配置深度流
    rs2::config config;
    config.enable_stream(RS2_STREAM_DEPTH, 640, 480, RS2_FORMAT_Z16, 30);

    // 开始捕获深度流
    rs2::pipeline pipeline;
    pipeline.start(config);

    // 捕获深度图像并获取深度值
    while (true) {
        rs2::frameset frames = pipeline.wait_for_frames();
        rs2::depth_frame depth_frame = frames.get_depth_frame();

        // 获取深度数据
        const int width = depth_frame.get_width();
        const int height = depth_frame.get_height();
        const uint16_t* depth_data = reinterpret_cast<const uint16_t*>(depth_frame.get_data());

        // 深度值
        const int x = width / 2; // 选择图像中心点
        const int y = height / 2;
        uint16_t depth_value = depth_data[y * width + x];
        std::cout << "Depth at center: " << depth_value << " millimeters" << std::endl;
    }

    return EXIT_SUCCESS;
}

