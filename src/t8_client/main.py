import os
from collections.abc import Callable

import click
import matplotlib.pyplot as plt
import numpy as np
from dotenv import load_dotenv

from t8_client.functions import (
    get_spectrum,
    get_spectrum_list,
    get_wave,
    get_waveform_list,
)

# Cargar el archivo .env
load_dotenv(dotenv_path="./.env")

# Definir una constante para los valores mágicos
HTTP_OK = 200


@click.group()
@click.pass_context
def main(ctx: click.Context) -> None:
    """
    Función principal que configura las variables de entorno.
    """
    ctx.ensure_object(dict)
    ctx.obj["T8_HOST"] = os.getenv("T8_HOST")
    ctx.obj["T8_USER"] = os.getenv("T8_USER")
    ctx.obj["T8_PASSWORD"] = os.getenv("T8_PASSWORD")
    print(f"T8_HOST: {ctx.obj['T8_HOST']}")
    print(f"T8_USER: {ctx.obj['T8_USER']}")
    print(f"T8_PASSWORD: {ctx.obj['T8_PASSWORD']}")


def pmode_params(func: Callable) -> Callable:

    func = click.option(
        "-M", "--machine", required=True, help="Machine tag"
    )(func)
    func = click.option(
        "-p", "--point", required=True, help="Point tag"
    )(func)
    func = click.option(
        "-m", "--pmode", required=True, help="Processing mode tag"
    )(func)
    return func


def parse_combined_tag(
    ctx: click.Context, param: click.Parameter | None, value: str
) -> str:
    """
    Analiza un valor combinado en el formato 'machine:point:pmode' descomponiendolo.
    """
    if value and ":" in value:
        machine, point, pmode = value.split(":")
        ctx.params["machine"] = machine
        ctx.params["point"] = point
        ctx.params["pmode"] = pmode
    return value


@main.command(
    name="list-waves",
    help="List waveforms for a specific machine, point, and processing mode.",
)
@pmode_params
@click.pass_context
def list_waves(ctx: click.Context, machine: str, point: str, pmode: str) -> None:
    """
    Listar las formas de onda para una máquina, punto y modo de procesamiento.
    """
    try:
        waves = get_waveform_list(
            t8_host=ctx.obj["T8_HOST"],
            machine=machine,
            point=point,
            pmode=pmode,
            t8_user=ctx.obj["T8_USER"],
            t8_password=ctx.obj["T8_PASSWORD"],
        )

        if waves:
            for wave in waves:
                print(wave)
        else:
            print("No waves found for the given parameters.")
    except Exception as e:
        print(f"Error retrieving waveforms: {e}")


@main.command(
    name="list-spectra",
    help="List spectra for a specific machine, point, and processing mode.",
)
@pmode_params
@click.pass_context
def list_spectra(ctx: click.Context, machine: str, point: str, pmode: str) -> None:
    """
    Listar los espectros para una máquina, punto y modo de procesamiento .
    """
    try:
        spectra = get_spectrum_list(
            t8_host=ctx.obj["T8_HOST"],
            machine=machine,
            point=point,
            pmode=pmode,
            t8_user=ctx.obj["T8_USER"],
            t8_password=ctx.obj["T8_PASSWORD"],
        )
        if spectra:
            for spectrum in spectra:
                print(spectrum)
        else:
            print("No spectra found for the given parameters.")
    except Exception as e:
        print(f"Error retrieving spectra: {e}")


@main.command(
    name="get-wave",
    help="Get the waveform data for a given machine, point, processing mode, and time.",
)
@pmode_params
@click.option("-t", "--time", required=True, help="Time of the wave (ISO format)")
@click.pass_context
def get_wave_command(
    ctx: click.Context, machine: str, point: str, pmode: str, time: str
) -> None:
    try:
        waveform, sample_rate = get_wave(
            t8_host=ctx.obj["T8_HOST"],
            machine=machine,
            point=point,
            pmode=pmode,
            time=time,
            t8_user=ctx.obj["T8_USER"],
            t8_password=ctx.obj["T8_PASSWORD"],
        )
        print(f"Sample Rate: {sample_rate} Hz")
        print(f"Waveform Data: {waveform}")

    except Exception as e:
        print(f"Error retrieving waveform: {e}")


@main.command(
    name="get-spectrum",
    help="Get the spectrum data for a given machine, point, processing mode, and time.",
)
@pmode_params
@click.option("-t", "--time", required=True, help="Time of the spectrum (ISO format)")
@click.pass_context
def get_spectrum_command(
    ctx: click.Context, machine: str, point: str, pmode: str, time: str
) -> None:

    try:
        spectrum = get_spectrum(
            t8_host=ctx.obj["T8_HOST"],
            machine=machine,
            point=point,
            pmode=pmode,
            time=time,
            t8_user=ctx.obj["T8_USER"],
            t8_password=ctx.obj["T8_PASSWORD"],
        )[0]
        spectrum_data = list(spectrum)

        if not spectrum_data:
            print("No data found in spectrum.")
            return
        print(f"Spectrum Data: {spectrum_data[:10]}...")
    except Exception as e:
        print(f"Error retrieving spectrum: {e}")


@main.command(
    name="plot-wave",
    help="Plot the waveform data for a machine, point, processing mode, and time.",
)
@pmode_params
@click.option("-t", "--time", required=True, help="Time of the wave (ISO format)")
@click.pass_context
def plot_wave(
    ctx: click.Context, machine: str, point: str, pmode: str, time: str
) -> None:
    """
    Graficar la forma de onda para una máquina, punto, modo de procesamiento y tiempo.
    """
    try:

        waveform, sample_rate = get_wave(
            t8_host=ctx.obj["T8_HOST"],
            machine=machine,
            point=point,
            pmode=pmode,
            time=time,
            t8_user=ctx.obj["T8_USER"],
            t8_password=ctx.obj["T8_PASSWORD"],
        )

        print(f"Sample Rate: {sample_rate} Hz")
        print(f"Waveform Data: {waveform}")

        plt.figure(figsize=(10, 6))
        plt.plot(waveform)
        plt.title(f"Waveform - {machine} - {point} - {pmode} - {time}")
        plt.xlabel("Sample Index")
        plt.ylabel("Amplitude")
        plt.grid(True)
        plt.show()

    except Exception as e:
        print(f"Error retrieving waveform: {e}")


@main.command(
    name="plot-spectrum",
    help="Plot the spectrum data for a machine, point, processing mode, and time.",
)
@pmode_params
@click.option("-t", "--time", required=True, help="Time of the spectrum (ISO format)")
@click.pass_context
def plot_spectrum_(
    ctx: click.Context, machine: str, point: str, pmode: str, time: str
) -> None:
    """
    Graficar el espectro para una máquina, punto, modo de procesamiento y tiempo.
    """
    if point and ":" in point:
        parse_combined_tag(ctx, None, point)
    spectrum, fmin, fmax = get_spectrum(
        t8_host=ctx.obj["T8_HOST"],
        machine=machine,
        point=point,
        pmode=pmode,
        time=time,
        t8_user=ctx.obj["T8_USER"],
        t8_password=ctx.obj["T8_PASSWORD"],
    )

    freqs = np.linspace(fmin, fmax, len(spectrum))
    plt.plot(freqs, spectrum)
    plt.xlim(fmin, fmax)
    plt.title(f"Spectrum - {machine} - {point} - {pmode} - {time}")
    plt.xlabel("Frequency (Hz)")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
