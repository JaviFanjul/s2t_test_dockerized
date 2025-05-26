import os
import re
import logging


# Basic logger configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def create_file(file_name):
    """
    Creates a new file or clears its contents if it already exists.

    Args:
        file_name (str): Path to the file to be created or cleared.
    """
    try:
        if os.path.exists(file_name):
            open(file_name, "w", encoding="utf-8").close()
        with open(file_name, 'w', encoding='utf-8') as file:
            pass
    except Exception as e:
        logging.error(f"Failed to create file {file_name}: {e}")

def delete_directory(output_folder):
    """
    Deletes all files inside the specified directory.

    Args:
        output_folder (str): Path to the directory to clean.
    """
    try:
        for name in os.listdir(output_folder):
            file_path = os.path.join(output_folder, name)
            os.remove(file_path)
    except Exception as e:
        logging.error(f"Failed to delete files in {output_folder}: {e}")

def load_context(file_name, n, rol):
    """
    Loads the last 'n' utterances from the given speaker as context, stripping timestamps and speaker tags.

    Args:
        file_name (str): Path to the transcription file.
        n (int): Number of utterances to include.
        rol (str): Role to filter by (e.g., "Cliente" or "Agente").

    Returns:
        str: Concatenated clean utterances to be used as context.
    """
    lines = []
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            all_lines = file.readlines()

        
        pattern = re.compile(rf"\(\d+\.\d+-\d+\.\d+\)\s*{rol}:(.*)")

        for line in reversed(all_lines):
            match = pattern.match(line.strip())
            if match:
                lines.append(match.group(1).strip())
            if len(lines) >= n:
                break

        return " ".join(reversed(lines))

    except FileNotFoundError:
        logging.warning(f"File not found: {file_name}")
        return ""
    except Exception as e:
        logging.error(f"Failed to load context from {file_name}: {e}")
        return ""

def extract_time(filename):
    """
    Extracts the time interval from a filename using a predefined pattern.

    Args:
        filename (str): Filename containing a time interval.

    Returns:
        str or None: The extracted time range (e.g., "12.0-15.2"), or None if not found.
    """
    match = re.search(r"chunk_\d+_(\d+\.\d+)-(\d+\.\d+)", filename)
    if match:
        start = match.group(1)
        end = match.group(2)
        return f"{start}-{end}"
    return None
