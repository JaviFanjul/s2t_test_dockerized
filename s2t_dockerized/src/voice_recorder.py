import numpy as np
import wave
import os
import time
from collections import deque
from config import *
from tools.list_audio_sources import list_audio_sources
from tools.Chronometer import Chronometer
from scipy.signal import butter, lfilter
import logging

class VoiceRecorder:
    """
    Records voice segments from a specific audio input device, using an RMS-based VAD
    and bandpass filtering to detect and save spoken audio chunks.

    Attributes:
        output_folder (str): Path to save recorded audio chunks.
        id_device (int): Index of the audio input device.
        p (pyaudio.PyAudio): PyAudio instance to manage audio streams.
        queue (Queue): Queue to send paths of saved audio chunks.
    """

    def __init__(self, output_folder, id_device, pyaudio_instance, queue):
        """
        Initializes the voice recorder with audio settings and queue references.

        Args:
            output_folder (str): Directory to save recorded chunks.
            id_device (int): Input device index from PyAudio.
            pyaudio_instance (PyAudio): Initialized PyAudio instance.
            queue (Queue): Output queue to send filenames of saved chunks.
        """
        self.output_folder = output_folder
        self.id_device = id_device
        self.p = pyaudio_instance
        self.queue = queue
        self.stream = None
        self.chronometer = Chronometer()
        self.chunk_count = 0

    def _bandpass_filter(self, data, lowcut=LOWCUT_FREQ, highcut=HIGHCUT_FREQ, fs=RATE, order=FILTER_ORDER):
        """
        Applies a bandpass filter to the raw audio signal.

        Args:
            data (np.ndarray): Raw audio data.
            lowcut (float): Low frequency cutoff.
            highcut (float): High frequency cutoff.
            fs (int): Sample rate.
            order (int): Filter order.

        Returns:
            np.ndarray: Filtered audio data.
        """
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        return lfilter(b, a, data)

    def start(self):
        """
        Starts the continuous voice recording loop with VAD and chunk saving logic.
        """
        try:
            self.stream = self.p.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index=self.id_device
            )

            pre_silence_queue = deque(maxlen=PRE_BUFFER)
            audio_queue = deque()

            recording = False
            post_silence_count = 0
            chunk_time = 0

            logging.info(f"[{self.id_device}] Using fixed threshold: {THRESHOLD}")
            logging.info("Listening... (Press Ctrl+C to stop)")

            self.chronometer.start()

            while True:
                start_time = time.time()
                data = self.stream.read(CHUNK, exception_on_overflow=False)
                audio_np = np.frombuffer(data, dtype=np.int16)
                audio_np = self._bandpass_filter(audio_np)
                rms = np.sqrt(np.mean(audio_np**2))

                if rms > THRESHOLD:
                    if not recording:
                        logging.info("Voice detected. Starting recording...")
                        beggining_time = self.chronometer.get_time()
                        recording = True
                        audio_queue.extend(pre_silence_queue)
                        chunk_time = 0
                    audio_queue.append(data)
                    post_silence_count = 0
                else:
                    if recording:
                        post_silence_count += 1
                        audio_queue.append(data)
                        if post_silence_count >= POST_BUFFER:
                            self._save_chunk(audio_queue, beggining_time)
                            audio_queue.clear()
                            recording = False
                    else:
                        pre_silence_queue.append(data)

                elapsed_time = time.time() - start_time
                chunk_time += elapsed_time

                if chunk_time >= MAX_CHUNK_TIME:
                    if recording:
                        self._save_chunk(audio_queue, beggining_time)
                        audio_queue.clear()
                        recording = False
                        chunk_time = 0

        except KeyboardInterrupt:
            logging.info("Stopping recording...")
            self._close_stream()

        except (OSError, IOError, RuntimeError) as e:
            logging.error(f"System error: {e}")
            list_audio_sources()

    def _save_chunk(self, audio_queue, beggining_time):
        """
        Saves the current audio chunk to disk and enqueues the filename.

        Args:
            audio_queue (deque): Buffer containing audio frames.
            beggining_time (float): Timestamp marking the start of the chunk.
        """
        self.chunk_count += 1
        chunk_filename = os.path.join(
            self.output_folder,
            f"chunk_{self.chunk_count}_{beggining_time}-{self.chronometer.get_time()}.wav"
        )

        with wave.open(chunk_filename, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(audio_queue))

        logging.info(f"Saved chunk #{self.chunk_count} for device {self.id_device}: {chunk_filename}")
        self.queue.put(chunk_filename)

    def _close_stream(self):
        """
        Closes the audio stream and terminates the PyAudio instance.
        """
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()
