/**
 * @projectName test
 * @file main.cpp
 * @brief 
 * 
 * @author yx 
 * @date 2023-10-05 22:11
 */

#include <spdlogger.h>

int main(int argc, char *argv[]) {
    spdlogger logger(__FUNCTION__);

    logger.info("KdRobotCppLibs compiled!");

    return 0;
}

