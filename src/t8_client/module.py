import csv
from base64 import b64decode
from datetime import datetime, timezone
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
    float_array = np.array(
        [
            unpack("h", decompressed_data[i * 2 : (i + 1) * 2])[0]
            for i in range(int(len(decompressed_data) / 2))
        ],
        dtype="f",
    )
    return float_array


def convert_unix_to_iso(timestamp: int) -> str:
    """
    Converts a Unix timestamp to an ISO 8601 date string in UTC.

    :param timestamp: The number of seconds since January 1, 1970 (Unix epoch).
    :return: The date and time in ISO 8601 format (YYYY-MM-DDTHH:MM:SS) in UTC.
    """
    utc_time = datetime.utcfromtimestamp(timestamp).replace(tzinfo=timezone.utc)
    return utc_time.strftime("%Y-%m-%dT%H:%M:%S")

def convert_iso_to_unix(iso_string: str) -> int:
    """
    Converts an ISO 8601 date string to a Unix timestamp, considering UTC.

    :param iso_string: The date and time in ISO 8601 format in UTC.
    :return: Unix timestamp (seconds since January 1, 1970).
    """
    iso_time = datetime.fromisoformat(iso_string).replace(tzinfo=timezone.utc)
    return int(iso_time.timestamp())

def url_generator(type, machine, point, pmode, year, month, day, hour, minute, second):
    """
    Generates the URL to access the T8 data, using environment variables.

    :param type: Type of data to access (waves, spectra, etc.)
    :param machine: Machine name
    :param point: Measurement point
    :param pmode: Processing mode
    :param year: Year of the date
    :param month: Month of the date
    :param day: Day of the date
    :param hour: Hour of the date
    :param minute: Minute of the date
    :param second: Second of the date
    :return: Full URL for making the request
    """
    utc_time = datetime(year, month, day, hour, minute, second, tzinfo=timezone.utc)
    timestamp = int(utc_time.timestamp())
    url = f"{host}/rest/{type}/{machine}/{point}/{pmode}/{timestamp}"

    return url

def save_array_to_csv(file_path, data, header=None):
    if isinstance(data, list) and isinstance(data[0], (list, tuple)):
        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            if header:
                writer.writerow([header])  # Escribir el encabezado, si existe
                writer.writerows(data)  # Escribir todas las filas
    elif isinstance(data, list) and isinstance(data[0], dict):
            # Si los datos son una lista de diccionarios
        with open(file_path, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            if header:
                writer.writeheader()
                writer.writerows(data)
