#!/bin/bash
# @brief: install necessary depend
# @time: 2023-6-7 13:00

echo "necessary depend installing..."
echo "(正在下载必要依赖...)"

sudo apt update
sudo apt install -y \
                    git \
                    vim \
                    cmake \
                    cmake-gui \
                    g++ \
                    gcc \
		    python3-pip \
		    zip \
		    unzip \
		    rar \
		    unrar \
		    tree \
      		    wget
	    
echo "necessary depend finished!"
