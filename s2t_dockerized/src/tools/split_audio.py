from pydub import AudioSegment
import os

def separar_canales_audio(carpeta_entrada, carpeta_salida_izq, carpeta_salida_der):
    # Crear carpetas de salida si no existen
    os.makedirs(carpeta_salida_izq, exist_ok=True)
    os.makedirs(carpeta_salida_der, exist_ok=True)

    # Recorrer los archivos de la carpeta de entrada
    for archivo in os.listdir(carpeta_entrada):
        if archivo.lower().endswith(('.wav', '.mp3', '.flac', '.ogg')):  # Filtrar solo archivos de audio
            ruta_completa = os.path.join(carpeta_entrada, archivo)
            
            # Cargar el audio
            audio = AudioSegment.from_file(ruta_completa)
            
            # Verificar si es estéreo
            if audio.channels == 2:
                canal_izquierdo = audio.split_to_mono()[0]
                canal_derecho = audio.split_to_mono()[1]
                
                # Guardar los canales en sus respectivas carpetas
                archivo_sin_extension = os.path.splitext(archivo)[0]
                ruta_izq = os.path.join(carpeta_salida_izq, f"{archivo_sin_extension}_L.wav")
                ruta_der = os.path.join(carpeta_salida_der, f"{archivo_sin_extension}_R.wav")

                canal_izquierdo.export(ruta_izq, format="wav")
                canal_derecho.export(ruta_der, format="wav")

                print(f"Procesado: {archivo}")

# Ejemplo de uso

audios_original = f"C:\\Users\\Javi\\Desktop\\MasOrange\\stereo_audios\\stereo_audios\wavs"
audios_derecha =f"C:\\Users\\Javi\\Desktop\\MasOrange\\stereo_audios\\stereo_audios\\audio_mono\\derecha"
audios_izquierda = f"C:\\Users\\Javi\\Desktop\\MasOrange\\stereo_audios\\stereo_audios\\audio_mono\\izquierda"

separar_canales_audio(audios_original, audios_izquierda, audios_derecha)
