import pyaudio

DEVICE_INDEX = 1  # Cambia este número si quieres probar otro dispositivo
CHANNELS = 1
FORMAT = pyaudio.paInt16
POSSIBLE_RATES = [8000, 11025, 16000, 22050, 32000, 44100, 48000, 96000]

p = pyaudio.PyAudio()
device_info = p.get_device_info_by_index(DEVICE_INDEX)
print(f"🎧 Probing device: {device_info['name']} (ID {DEVICE_INDEX})")
print("Supported sample rates:")

for rate in POSSIBLE_RATES:
    try:
        if p.is_format_supported(rate,
                                 input_device=DEVICE_INDEX,
                                 input_channels=CHANNELS,
                                 input_format=FORMAT):
            print(f"✅ {rate} Hz")
    except Exception as e:
        print(f"❌ {rate} Hz - {e}")

p.terminate()
