import logging
from faster_whisper import WhisperModel
from config import *

import logging
from faster_whisper import WhisperModel
from config import *

class ModelLoader:
    """
    This class is responsible for loading a Whisper model with custom parameters.

    Attributes:
        model_name (str): The name of the Whisper model to load.
        device (str): The device to run the model on (e.g., "cpu", "cuda").
        compute_type (str): The type of computation (e.g., "int8", "float32").
        language (str): The language of the audio to transcribe.
    """

    def __init__(self, model_name=whisper_model, device=device, compute_type=compt, language=language):
        """
        Initializes the model loader with the required parameters.

        Args:
            model_name (str): Whisper model name.
            device (str): Execution device ("cpu", "cuda", etc.).
            compute_type (str): Precision of computation.
            language (str): Language of the input audio.
        """
        self.model_name = model_name
        self.device = device
        self.compute_type = compute_type
        self.language = language

    def load(self):
        """
        Loads the Whisper model using the configured parameters.

        Returns:
            tuple: The loaded Whisper model and the transcription options.

        Raises:
            Exception: If an error occurs while loading the model.
        """
        try:
            logging.info("Loading Whisper model...")

            # Create the model instance with the provided parameters
            model = WhisperModel(
                self.model_name,
                device=self.device,
                compute_type=self.compute_type
            )

            # Transcription options to be used with the model
            options = {
                "task": "transcribe",
                "language": self.language
            }

            logging.info("Whisper model loaded successfully.")
            return model, options

        except Exception as e:
            logging.error(f"Failed to load Whisper model: {e}")
            raise
