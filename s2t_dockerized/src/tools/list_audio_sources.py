import pyaudio

def list_audio_sources():
    p = pyaudio.PyAudio()

    print("=== Available audio input devices ===")
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        print(f"[{i}] {info['name']} - {info['maxInputChannels']} channels")

    p.terminate()
