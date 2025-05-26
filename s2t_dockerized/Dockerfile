FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

WORKDIR /app

# Instala dependencias del sistema (incluye libpulse-dev sin error)
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    ffmpeg \
    build-essential \
    libasound-dev \
    portaudio19-dev \
    libportaudiocpp0 \
    libpulse-dev \
    pulseaudio-utils \
    alsa-utils \
    python3-dev \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Actualiza pip e instala wheel
RUN python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel

 #Compilar PortAudio manualmente con soporte PulseAudio
WORKDIR /tmp
RUN git clone https://github.com/PortAudio/portaudio.git && \
    cd portaudio && \
    ./configure --with-pulseaudio && \
    make -j$(nproc) && \
    make install && \
    ldconfig

# Instalar PyAudio manualmente contra PortAudio recién compilado
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-binary :all: pyaudio

WORKDIR /app
# Instala tus otras dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Copiando codigo
COPY src/ ./src/
COPY transcription.txt .
COPY chunks_sp1/ ./chunks_sp1/
COPY chunks_sp2/ ./chunks_sp2/
COPY config/ ./config/

# Copia el script de ejecución
COPY run.sh .
RUN chmod +x run.sh

# CMD comentado por ahora para lanzar con bash en pruebas
# CMD ["./run.sh"]
