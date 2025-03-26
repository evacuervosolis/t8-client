import numpy as np
import requests

from t8_client.module import (
    convert_iso_to_unix,
    convert_unix_to_iso,
    decode_and_convert_to_float,
)


def get_waveform_list(**params):
    """
    This function is used to fetch a list of timestamps for wave data from
    a specified server and endpoint.

    Parameters:
        **params: A collection of named arguments (also known as keyword arguments).
            host (str): The URL of the server you are connecting to.
            id_ (str): The unique identifier for the endpoint you're accessing.
            machine (str): The identifier for the machine from which data
            is being retrieved.
            point (str): The identifier for the measurement point on the machine.
            pmode (str): The processing mode you're working with.
            t8_user (str): The username required to authenticate with the server.
            t8_password (str): The password corresponding to the username
             for authentication.

    Yields:
        str: ISO formatted timestamp string for each valid wave entry.
        This function generates (yields) timestamps one at a time as it fetches them.

    Raises:
        Exception: If there is an issue with the request
        (e.g., the server fails to respond or returns an error),
                   the function will raise an exception.
    """
    t8_host = params["t8_host"]
    machine = params["machine"]
    point = params["point"]
    pmode = params["pmode"]
    t8_user = params["t8_user"]
    t8_password = params["t8_password"]

    url = f"{t8_host}/rest/waves/{machine}/{point}/{pmode}"
    response = requests.get(url, auth=(t8_user, t8_password))
    if response.status_code != 200:
        raise Exception(f"Failed to get waveform: {response.text}")
    response = response.json()

    for item in response["_items"]:
        timestamp = int(item["_links"]["self"].split("/")[-1])
        if timestamp != 0:
            yield convert_unix_to_iso(timestamp)


def get_spectrum_list(**params):
    """
    Retrieves a list of spectrums from a specified host and endpoint.

    Args:
        **params: Arbitrary keyword arguments.
            host (str): The host URL.
            id_ (str): The ID for the endpoint.
            machine (str): The machine identifier.
            point (str): The point identifier.
            pmode (str): The mode parameter.
            t8_user (str): The username for authentication.
            t8_password (str): The password for authentication.

    Yields:
        str: ISO formatted timestamp string for each valid wave item.

    Raises:
        Exception: If the request to the server fails.
    """
    t8_host = params["t8_host"]
    machine = params["machine"]
    point = params["point"]
    pmode = params["pmode"]
    t8_user = params["t8_user"]
    t8_password = params["t8_password"]

    url = f"{t8_host}/rest/spectra/{machine}/{point}/{pmode}"
    response = requests.get(url, auth=(t8_user, t8_password))
    if response.status_code != 200:
        raise Exception(f"Failed to get spectra list: {response.text}")
    response = response.json()

    for item in response["_items"]:
        timestamp = int(item["_links"]["self"].split("/")[-1])
        if timestamp != 0:
            yield convert_unix_to_iso(timestamp)


def get_wave(**params) -> tuple[np.ndarray, int]:
    """
    Retrieves waveform data from a specified host.

    Arguments:
        kwargs: A set of keyword arguments representing the URL
        parameters needed for the request.

    Returns:
        tuple[np.ndarray, int]: This function returns a tuple where:
            - The first element is a numpy array containing the waveform data.
            - The second element is an integer representing the sample rate.

    Raises:
        Exception: If the server request to fetch the waveform data is unsuccessful.
    """
    t8_host = params["t8_host"]
    machine = params["machine"]
    point = params["point"]
    pmode = params["pmode"]
    time = convert_iso_to_unix(params["time"])
    t8_user = params["t8_user"]
    t8_password = params["t8_password"]

    url = f"{t8_host}/rest/waves/{machine}/{point}/{pmode}/{time}"
    response = requests.get(url, auth=(t8_user, t8_password))
    if response.status_code != 200:
        raise Exception(f"Failed to get waveform: {response.text}")
    response = response.json()

    waveform = decode_and_convert_to_float(response["data"])
    factor = response["factor"]
    sample_rate = response["sample_rate"]

    return waveform * factor, sample_rate


def get_spectrum(**params) -> tuple[np.ndarray]:
    """
    Retrieves spectral data from a given host and endpoint.

    Arguments:
        params: A collection of keyword arguments that represent the URL parameters for the request.

    Returns:
        tuple[np.ndarray]: A tuple where:
            - The first element is a numpy array containing the spectral data.

    Raises:
        Exception: If the server request to fetch the spectral data fails.
    """
    t8_host = params["t8_host"]
    machine = params["machine"]
    point = params["point"]
    pmode = params["pmode"]
    time = convert_iso_to_unix(params["time"])
    t8_user = params["t8_user"]
    t8_password = params["t8_password"]

    url = f"{t8_host}/rest/spectra/{machine}/{point}/{pmode}/{time}"
    response = requests.get(url, auth=(t8_user, t8_password))
    if response.status_code != 200:
        raise Exception(f"Failed to get spectra: {response.text}")
    response = response.json()

    spectrum = decode_and_convert_to_float(response["data"])
    factor = response["factor"]
    min_freq = response.get("min_freq", 0)
    max_freq = response["max_freq"]

    return spectrum * factor, min_freq, max_freq
