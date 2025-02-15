FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=America/Mexico_City

RUN apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common \
    tzdata \
    curl \
    ffmpeg \
 && add-apt-repository ppa:deadsnakes/ppa \
 && apt-get update && apt-get install -y --no-install-recommends \
    python3.11 \
    python3.11-venv \
    python3.11-distutils \
 && rm -rf /var/lib/apt/lists/*
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 && \
 update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1
 
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

RUN curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp \
    -o /usr/local/bin/yt-dlp && chmod a+rx /usr/local/bin/yt-dlp

WORKDIR /app
COPY . /app

RUN python3.11 -m pip install --upgrade pip && python3.11 -m pip install -r requirements.txt

EXPOSE 8080

# Comando de inicio de la aplicación
CMD ["python3.11", "new_ascii.py"]
