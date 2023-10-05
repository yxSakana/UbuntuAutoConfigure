/**
 * @projectName test
 * @file main.cpp
 * @brief 
 * 
 * @author yx 
 * @date 2023-10-05 22:11
 */

#include <iostream>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>

int main(int argc, char *argv[]) {
    cv::Mat img = cv::imread("../../img/img.png", cv::IMREAD_COLOR);
    if (!img.empty()) {
        cv::imshow("img", img);
        cv::waitKey(0);
    } else {
        std::cerr << "路径错误! 图像未打开!(img/img.png)\n";
    }

    return 0;
}

