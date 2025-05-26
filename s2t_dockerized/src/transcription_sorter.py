import re
import time
import os
import logging

class TranscriptionSorter:
    """
    Periodically sorts a transcription file based on timestamps to ensure chronological order.

    Attributes:
        file_path (str): Path to the transcription file to be sorted.
        interval (int): Time interval (in seconds) between sorting operations.
    """

    def __init__(self, file_path, interval=5):
        """
        Initializes the sorter with the file path and sorting interval.

        Args:
            file_path (str): Path to the transcription file.
            interval (int): Time interval between sort executions (in seconds).
        """
        self.file_path = file_path
        self.interval = interval

    def _extract_time_and_text(self, line):
        """
        Extracts the start and end times, and the transcription text from a line.

        Args:
            line (str): A line from the transcription file.

        Returns:
            tuple: ((start_time, end_time), text) if pattern matched, otherwise (None, stripped_line).
        """
        match = re.match(r"\((\d+\.\d+)-(\d+\.\d+)\)(.*)", line)
        if match:
            start = float(match.group(1))
            end = float(match.group(2))
            text = match.group(3).strip()
            return (start, end), text
        return None, line.strip()

    def _sort_transcriptions_in_file(self):
        """
        Reads, sorts, and rewrites the transcription file based on start timestamps.
        Groups entries in 5-second intervals for better structure.
        """
        if not os.path.exists(self.file_path):
            logging.warning(f"File not found: {self.file_path}")
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()

            # Extract and filter valid transcriptions
            transcriptions = [self._extract_time_and_text(line) for line in lines]
            transcriptions = [item for item in transcriptions if item[0] is not None]
            transcriptions.sort(key=lambda x: x[0][0])  # Sort by start time

            # Group transcriptions in 5-second intervals
            grouped = {}
            for (start, end), text in transcriptions:
                key = int(start // 5) * 5
                grouped.setdefault(key, []).append(((start, end), text))

            # Rewrite the sorted file
            with open(self.file_path, "w", encoding="utf-8") as file:
                for start_time in sorted(grouped.keys()):
                    for (start, end), text in sorted(grouped[start_time], key=lambda x: x[0][0]):
                        file.write(f"({start}-{end}) {text}\n")

        except Exception as e:
            logging.error(f"Failed to sort transcriptions: {e}")

    def start(self):
        """
        Starts the periodic sorting loop that checks and rewrites the file at a given interval.
        """
        try:
            while True:
                self._sort_transcriptions_in_file()
                time.sleep(self.interval)
        except KeyboardInterrupt:
            logging.warning("Transcription sorter manually interrupted.")
        except Exception as e:
            logging.error(f"Unexpected error in sorter thread: {e}")
