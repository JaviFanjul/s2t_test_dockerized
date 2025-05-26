import pyaudio

p = pyaudio.PyAudio()

for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    if dev['maxOutputChannels'] > 0:  # Solo mostrar dispositivos de salida
        print(f"ID {i}: {dev['name']} - Channels: {dev['maxOutputChannels']}")

p.terminate()

