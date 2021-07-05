FROM python:3.8-slim

RUN apt-get update && \
    apt-get install -qy --no-install-recommends \
    # gcc python3 python3-dev python3-pip libatlas-base-dev python3-h5py libfreetype6 libharfbuzz0b && \
    libopencv-dev python-opencv &&\
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY app/requirements.txt .
RUN python3 -m pip install -r requirements.txt
COPY app .

CMD ["python3", "bot.py"]