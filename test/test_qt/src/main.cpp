/**
 * @projectName test
 * @file main.cpp
 * @brief 
 * 
 * @author yx 
 * @date 2023-10-05 22:11
 */

#include <QApplication>
#include <QPushButton>

int main(int argc, char *argv[]) {
    QApplication a(argc, argv);

    QPushButton button("Hello world!", nullptr);
    button.resize(200, 100);
    button.show();

    return QApplication::exec();
}

