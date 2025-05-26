#!/bin/bash

set -e

echo "[INFO] Starting PulseAudio..."
pulseaudio -D --exit-idle-time=-1

# Esperar a que pulse arranque
sleep 2

# Verificar si existen los sinks
if pactl list short sinks | grep -q "client_sink"; then
    echo "[INFO] Sink 'client_sink' already exists. Skipping creation."
else
    echo "[INFO] Creating 'client_sink'..."
    pactl load-module module-null-sink sink_name=client_sink sink_properties=device.description=ClientSink
fi

if pactl list short sinks | grep -q "agent_sink"; then
    echo "[INFO] Sink 'agent_sink' already exists. Skipping creation."
else
    echo "[INFO] Creating 'agent_sink'..."
    pactl load-module module-null-sink sink_name=agent_sink sink_properties=device.description=AgentSink
fi

# Verificar si existen los sources
if pactl list short sources | grep -q "client_mic"; then
    echo "[INFO] Source 'client_mic' already exists. Skipping creation."
else
    echo "[INFO] Creating 'client_mic'..."
    pactl load-module module-remap-source master=client_sink.monitor source_name=client_mic
fi

if pactl list short sources | grep -q "agent_mic"; then
    echo "[INFO] Source 'agent_mic' already exists. Skipping creation."
else
    echo "[INFO] Creating 'agent_mic'..."
    pactl load-module module-remap-source master=agent_sink.monitor source_name=agent_mic
fi

python3 split_audio.py "stereo.wav" "left.wav" "right.wav"
python3 sound_player