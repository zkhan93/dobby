FROM debian:10.9-slim

RUN apt-get update && \
    apt-get install -qy --no-install-recommends \
    ca-certificates build-essential cmake git pkg-config libgtk-3-dev "libcanberra-gtk*"\
    libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev\
    libjpeg-dev libpng-dev libtiff-dev gfortran openexr libatlas-base-dev opencl-headers\
    python3-dev python3-numpy libtbb2 libtbb-dev libdc1394-22-dev &&\
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /opencv_source

RUN git clone --depth 1 --branch 3.4.14 https://github.com/opencv/opencv.git
RUN git clone --depth 1 --branch 3.4.14 https://github.com/opencv/opencv_contrib.git

WORKDIR /opencv_source/opencv/build
RUN cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_C_EXAMPLES=OFF \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D OPENCV_GENERATE_PKGCONFIG=ON \
    -D ENABLE_NEON=ON \
    -D OPENCV_EXTRA_EXE_LINKER_FLAGS=-latomic \
    -D ENABLE_VFPV3=ON \
    -D BUILD_TESTS=OFF \
    -D OPENCV_ENABLE_NONFREE=ON \
    -D OPENCV_EXTRA_MODULES_PATH=/opencv_source/opencv_contrib/modules \
    -D BUILD_EXAMPLES=OFF ..

RUN make -j4
RUN make install

RUN apt-get update && \
    apt-get install -qy --no-install-recommends \
    python3-pip python3-setuptools python3-wheel &&\
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY app/requirements.txt .

RUN python3 -m pip install -r requirements.txt

COPY app .
VOLUME ["/data"]
CMD ["python3", "/app/run.py"]