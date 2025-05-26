import logging
from utils import load_context, extract_time
from config import *

class Transcriber:
    """
    Transcribes audio files using a Whisper model and sends the output to a sink queue.

    Attributes:
        queue (Queue): Queue from which audio file paths are received.
        model (WhisperModel): Whisper model instance for transcription.
        options (dict): Options for the transcription process (e.g., language, task).
        output_file (str): Path to the output file used to extract conversation context.
        speaker (str): Speaker label to tag each transcription.
        sink_queue (Queue): Queue to send the transcribed text segments.
    """

    def __init__(self, queue, model, options, output_file, speaker, sink_queue):
        """
        Initializes the transcriber with model and transcription parameters.

        Args:
            queue (Queue): Queue containing paths to audio segments.
            model (WhisperModel): Instance of the model to be used for transcription.
            options (dict): Whisper model options (e.g., task type and language).
            output_file (str): File used to extract context from previous transcriptions.
            speaker (str): Label to prefix the transcription with (e.g., "Speaker 1").
            sink_queue (Queue): Queue to forward transcribed segments to be written.
        """
        self.queue = queue
        self.model = model
        self.options = options
        self.output_file = output_file
        self.speaker = speaker
        self.sink_queue = sink_queue

    def start(self):
        """
        Starts the transcription loop, continuously processing audio from the queue.
        Each segment is transcribed and sent to the sink queue with timestamp and speaker label.
        """
        try:
            while True:
                item = self.queue.get()
                try:
                    if item is None:
                        break  # Exit signal

                    # Extract timestamp from the filename
                    time_stamp = extract_time(item)
                    if time_stamp is None:
                        logging.warning(f"Could not extract timestamp from: {item}")
                        continue

                    # Load previous context for better transcription quality
                    context = load_context(self.output_file, numSeg, self.speaker)

                    vad_params = {
                        "threshold": threshold,
                        "min_speech_duration_ms": min_speech_duration,
                    }

                    # Transcribe the audio segment using VAD and context
                    segments, _ = self.model.transcribe(
                        item,
                        initial_prompt=context,
                        vad_filter=True,
                        vad_parameters=vad_params,
                        **self.options
                    )

                    # Format each segment and push to the sink queue
                    for segment in segments:
                        self.sink_queue.put(f"({time_stamp}){self.speaker}:{segment.text}\n")

                except Exception as e:
                    logging.error(f"Error while transcribing {item}: {e}")
                finally:
                    self.queue.task_done()

        except KeyboardInterrupt:
            logging.warning("Transcriber manually interrupted.")
        except Exception as e:
            logging.error(f"Unexpected error in transcriber thread: {e}")
