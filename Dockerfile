FROM jitesoft/tesseract-ocr
RUN train-lang nld --fast

USER root

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-tk && \
    apt-get clean

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT []

CMD ["python3", "main.py"]
