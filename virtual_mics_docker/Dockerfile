FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Instalación de herramientas y cabeceras necesarias
RUN apt-get update && apt-get install -y \
    pulseaudio \
    pulseaudio-utils \
    sox \
    ffmpeg \
    alsa-utils \
    python3 \
    python3-pip \
    wget \
    curl \
    git \
    libasound-dev \
    libpulse-dev \
    portaudio19-dev \
    python3-dev \
    && apt-get clean

# Compilación manual de PortAudio con soporte PulseAudio
RUN git clone https://github.com/PortAudio/portaudio.git /tmp/portaudio && \
    cd /tmp/portaudio && \
    ./configure --with-pulseaudio && \
    make -j$(nproc) && \
    make install && \
    ldconfig && \
    rm -rf /tmp/portaudio

# Instalación de PyAudio enlazado al PortAudio compilado
RUN pip install --no-binary :all: pyaudio

# Establecer directorio de trabajo final
WORKDIR /app

# Copiar y filtrar dependencias, sin sobrescribir PyAudio
COPY requirements.txt .
RUN grep -v "pyaudio" requirements.txt > filtered_requirements.txt
RUN pip install --no-cache-dir -r filtered_requirements.txt

# Copiar archivos del proyecto
COPY src/list_audio_sources.py ./src/
COPY src/split_audio.py ./src/
COPY audio/stereo.wav ./audio/
COPY src/sound_player.py ./src/
COPY start.sh .

# Hacer ejecutable el script de arranque si lo deseas
RUN chmod +x start.sh
ENTRYPOINT ["bash", "start.sh"]

