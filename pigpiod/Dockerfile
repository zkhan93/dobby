FROM balenalib/rpi-raspbian

RUN apt-get update &&\
    apt-get install -yq --no-install-recommends\
    pigpio &&\
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy and Start app
ADD start.sh /start.sh
CMD ["bash", "./start.sh"]