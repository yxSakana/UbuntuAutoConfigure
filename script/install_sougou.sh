#!/bin/bash

set -e
echo "开始安装搜狗输入法..."

# 1. 安装必要依赖
sudo apt update
sudo apt install -y fcitx gdebi wget

# 2. 下载搜狗输入法安装包
SOUGO_DEB="sogou-pinyin.deb"
SOUGOU_DEB_URL="https://ime-sec.gtimg.com/202507152337/e12e688e289223a6a8bd58bce4895a57/pc/dl/gzindex/1680521603/sogoupinyin_4.2.1.145_amd64.deb"
if [ ! -f "$SOUGO_DEB" ]; then
    echo "下载搜狗输入法安装包..."
    wget -c ${SOUGOU_DEB_URL}
fi

# 3. 安装搜狗输入法
echo "安装搜狗输入法..."
sudo gdebi -n $SOUGO_DEB

# 4. 配置输入法环境变量为fcitx
echo "配置输入法环境为 fcitx..."
im-config -n fcitx

# 5. 设置fcitx开机自启动
sudo cp /usr/share/applications/fcitx.desktop /etc/xdg/autostart/
#if ! grep -q "GTK_IM_MODULE=fcitx" ~/.bashrc; then
#    echo "export GTK_IM_MODULE=fcitx" >> ~/.bashrc
#    echo "export QT_IM_MODULE=fcitx" >> ~/.bashrc
#    echo "export XMODIFIERS=@im=fcitx" >> ~/.bashrc
#fi

# 6. Qt依赖
echo "Qt依赖..."
sudo apt install libqt5qml5 libqt5quick5 libqt5quickwidgets5 qml-module-qtquick2 -y
sudo apt install libgsettings-qt1 -y

echo "搜狗输入法安装完成，请注销后重新登录以生效。"
