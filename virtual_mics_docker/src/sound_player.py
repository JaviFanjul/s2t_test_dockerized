import wave
import pyaudio
import logging
import threading
import time

logging.basicConfig(level=logging.INFO)

def get_device_index_by_name(name_fragment, p, is_output=True):
    """
    Finds a PyAudio device index by matching a name fragment.

    Args:
        name_fragment (str): Substring of the device name to match.
        p (pyaudio.PyAudio): Shared PyAudio instance.
        is_output (bool): True to search for output devices.

    Returns:
        int: The device index if found, or None.
    """
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        name = info.get("name", "").lower()
        if name_fragment.lower() in name:
            if is_output and info["maxOutputChannels"] > 0:
                return i
            elif not is_output and info["maxInputChannels"] > 0:
                return i
    return None

def play_audio(file_path, device_name_fragment):
    """
    Plays a WAV file to the output device matching the given name fragment.

    Args:
        file_path (str): Path to the WAV file.
        device_name_fragment (str): Substring of the output device name.
    """
    try:
        # Crear PyAudio dentro del hilo para evitar inicialización recursiva
        p = pyaudio.PyAudio()
        index = get_device_index_by_name(device_name_fragment, p, is_output=True)

        if index is None:
            logging.error(f"No device where found '{device_name_fragment}'")
            p.terminate()
            return

        wf = wave.open(file_path, 'rb')
        info = p.get_device_info_by_index(index)
        channels = min(wf.getnchannels(), int(info["maxOutputChannels"]))

        stream = p.open(
            format=p.get_format_from_width(wf.getsampwidth()),
            channels=channels,
            rate=wf.getframerate(),
            output=True,
            output_device_index=index
        )

        logging.info(f"reproducing'{file_path}'in device#{index} ({info['name']})")

        chunk = 1024
        data = wf.readframes(chunk)
        while data:
            stream.write(data)
            data = wf.readframes(chunk)

        stream.stop_stream()
        stream.close()
        wf.close()
        p.terminate()

    except Exception as e:
        logging.error(f"Reproducction error: {e}")

def threaded_play(file, device_fragment):
    play_audio(file, device_fragment)

if __name__ == "__main__":
    # Crear los hilos para reproducir cada archivo en paralelo
    thread1 = threading.Thread(target=threaded_play, args=("audio/right.wav", "ClientSink"))
    thread2 = threading.Thread(target=threaded_play, args=("audio/left.wav", "AgentSink"))

    thread1.start()
    time.sleep(0.5)  # Pausa para evitar colisión de backend
    thread2.start()

    thread1.join()
    thread2.join()
