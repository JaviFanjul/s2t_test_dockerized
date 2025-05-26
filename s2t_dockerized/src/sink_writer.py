import logging
import os

class SinkWriter:
    """
    A component responsible for writing transcribed text segments to a file.

    Attributes:
        queue (Queue): A thread-safe queue containing transcription segments.
        file_path (str): Path to the output file where segments will be appended.
    """

    def __init__(self, queue, file_path):
        """
        Initializes the sink writer with the provided queue and output file path.

        Args:
            queue (Queue): Queue from which transcription segments are received.
            file_path (str): Path to the file where the transcriptions will be stored.
        """
        self.queue = queue
        self.file_path = file_path

    def start(self):
        """
        Continuously reads segments from the queue and writes them to the output file.
        Handles graceful shutdown and logs any errors during the process.
        """
        try:
            # Ensure the output directory exists
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

            while True:
                segment = self.queue.get()
                try:
                    if segment is None:
                        break  # Exit condition

                    with open(self.file_path, "a", encoding="utf-8") as f:
                        f.write(segment)

                except Exception as e:
                    logging.error(f"Failed to write segment: {e}")
                finally:
                    self.queue.task_done()

        except KeyboardInterrupt:
            logging.warning("Sink manually interrupted.")
        except Exception as e:
            logging.error(f"Unexpected error in sink thread: {e}")
