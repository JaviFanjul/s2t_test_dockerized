
import pyaudio
import wave
import threading


def play_to_virtual_mic(p,audio_file, output_device_index):
    wf = wave.open(audio_file, 'rb')

    # Verificar los canales soportados
    device_info = p.get_device_info_by_index(output_device_index)
    max_channels = device_info["maxOutputChannels"]
    channels = min(wf.getnchannels(), max_channels)  # Ajusta los canales al dispositivo

    print(f"Reproduciendo {audio_file} en dispositivo {output_device_index} con {channels} canales")

    stream = p.open(
        format=p.get_format_from_width(wf.getsampwidth()),
        channels=channels,
        rate=wf.getframerate(),
        output=True,
        output_device_index=output_device_index
    )

    chunk = 1024
    data = wf.readframes(chunk)

    while data:
        stream.write(data)  
        data = wf.readframes(chunk)

    stream.stop_stream()
    stream.close()
    wf.close()
    p.terminate()

p = pyaudio.PyAudio()
# Ajusta según los IDs reales de los dispositivos Virtual Audio Cable
virtual_mic_1 = 7  # Cambia por el ID correcto de "Line 1 (Virtual Audio Cable)"
virtual_mic_2 = 11  # Cambia por el ID correcto de "Line 2 (Virtual Audio Cable)"

audio1 = "C:\\Users\\Javi\\Desktop\\MasOrange\\stereo_audios\\stereo_audios\\audio_mono\\derecha\\9154631855480006851_R.wav"
audio2 ="C:\\Users\\Javi\\Desktop\\MasOrange\\stereo_audios\\stereo_audios\\audio_mono\\izquierda\\9154631855480006851_L.wav"
# Lanzar dos hilos para reproducir los audios en paralelo
thread1 = threading.Thread(target=play_to_virtual_mic, args=(p,audio1, virtual_mic_1))
thread2 = threading.Thread(target=play_to_virtual_mic, args=(p,audio2, virtual_mic_2))

thread1.start()
thread2.start()

thread1.join()
thread2.join()
