import csv
from base64 import b64decode
from datetime import UTC, datetime
from struct import unpack
from zlib import decompress

import numpy as np


def decode_and_convert_to_float(raw_data: str) -> np.ndarray:
    """
    This function takes a raw string (base64 encoded), decompresses it, and
    converts the data into a float array.

    :param raw_data: Base64 encoded string
    :return: A float array with the decompressed data
    """
    decompressed_data = decompress(b64decode(raw_data.encode()))
    return np.array(
        [
            unpack("h", decompressed_data[i * 2 : (i + 1) * 2])[0]
            for i in range(int(len(decompressed_data) / 2))
        ],
        dtype="f",
    )

def convert_unix_to_iso(timestamp: int) -> str:
    """
    Converts a Unix timestamp to an ISO 8601 date string in UTC.

    :param timestamp: The number of seconds since January 1, 1970 (Unix epoch).
    :return: The date and time in ISO 8601 format (YYYY-MM-DDTHH:MM:SS) in UTC.
    """
    utc_time = datetime.utcfromtimestamp(timestamp).replace(tzinfo=UTC)
    return utc_time.strftime("%Y-%m-%dT%H:%M:%S")

def convert_iso_to_unix(iso_string: str) -> int:
    """
    Converts an ISO 8601 date string to a Unix timestamp, considering UTC.

    :param iso_string: The date and time in ISO 8601 format in UTC.
    :return: Unix timestamp (seconds since January 1, 1970).
    """
    iso_time = datetime.fromisoformat(iso_string).replace(tzinfo=UTC)
    return int(iso_time.timestamp())

def save_array_to_csv(file_path: str, data: list, header: str | None = None) -> None:
    """
    Saves a list of data to a CSV file.

    :param file_path: Path where the file will be saved
    :param data: Data to be written (list of lists, tuples, or dictionaries)
    :param header: Optional header for the CSV
    :return: None
    """
    if isinstance(data, list) and isinstance(data[0], (list | tuple)):
        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            if header:
                writer.writerow([header])  # Write the header, if it exists
            writer.writerows(data)  # Write all rows
    elif isinstance(data, list) and isinstance(data[0], dict):
        with open(file_path, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            if header:
                writer.writeheader()
            writer.writerows(data)
