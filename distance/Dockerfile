FROM python:3.8-slim

RUN apt-get update && \
    apt-get install -yq --no-install-recommends \
    gcc python3-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY app/requirements.txt .
RUN pip install -r requirements.txt

COPY app .

CMD ["python", "run.py"]