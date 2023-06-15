#!/bin/bash
if [ ! -e ~/Downloads/Vision/ ]
then
  mkdir -p ~/Downloads/Vision/
fi

# kdrobotlibs
if [ ! -e ~/Downloads/Vision/kdrobotcpplibs ]
then
  echo "kdrobotcpplibs copying" && cp -r kdrobotcpplibs ~/Downloads/Vision/
fi
# opencv
if [ ! -e ~/Downloads/Vision/opencv/ ]
then
  mkdir -p ~/Downloads/Vision/opencv
fi

if [ ! -e ~/Downloads/Vision/opencv/opencv-4.5.0.zip ]
then
  echo "opencv copying" && cp OpenCV/opencv-4.5.0.zip ~/Downloads/Vision/opencv
fi

if [ ! -e ~/Downloads/Vision/opencv/opencv_contrib-4.5.0.tar.gz ]
then
  echo "opencv_contrib copying" && cp OpenCV/opencv_contrib-4.5.0.tar.gz ~/Downloads/Vision/opencv
fi
# typora
if [ ! -e ~/Downloads/Vision/typora1.2.4_Linux.rar ]
then
  echo "typora copying" && cp typora/typora1.2.4_Linux.rar ~/Downloads/Vision/
fi

cd ~/Downloads/Vision/opencv
unzip opencv-4.5.0.zip
tar -xzvf opencv_contrib-4.5.0.tar.gz
rm -rf opencv-4.5.0.zip opencv_contrib-4.5.0.tar.gz

cd ../
if [ ! -e typora/ ]
then
  mkdir typora
fi
unrar e "typora1.2.4_Linux.rar" -d typora
cd typora
# install
sudo dpkg -i typora_1.2.4_amd64.deb
# replace asar
sudo cp app.asar /usr/share/typora/resources && cd ..
# rm tmp
rm -rf typora
