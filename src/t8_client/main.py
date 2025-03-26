import os

import click
import matplotlib.pyplot as plt

from t8_client.functions import (
    get_spectrum,
    get_spectrum_list,
    get_wave,
    get_waveform_list,
)
from t8_client.module import save_array_to_csv


@click.group()
@click.pass_context
def main(ctx):
    ctx.ensure_object(dict)
    ctx.obj["T8_HOST"] = os.getenv("T8_HOST")  
    ctx.obj["T8_USER"] = os.getenv("T8_USER")  
    ctx.obj["T8_PASSWORD"] = os.getenv("T8_PASSWORD")  
    print(f"T8_HOST: {ctx.obj['T8_HOST']}")


def pmode_params(func):
    func = click.option("-M", "--machine", required=True, help="Machine tag")(func)
    func = click.option("-p", "--point", required=True, help="Point tag")(func)
    func = click.option("-m", "--pmode", required=True, help="Processing mode tag")(func)
    return func

@main.command(
    name="list-waves",
    help="List the available waveforms for a specific machine, point, and processing mode.",
)
@pmode_params
@click.pass_context
def list_waves(ctx, machine, point, pmode):
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
    help="List the available spectra for a specific machine, point, and processing mode.",
)
@pmode_params
@click.pass_context
def list_spectra(ctx, machine, point, pmode):
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
def get_wave_command(ctx, machine, point, pmode, time):
    try:
        waveform, sample_rate = get_wave(
            t8_host=ctx.obj["T8_HOST"],
            machine=machine,
            point=point,
            pmode=pmode,
            time=time,
            t8_user=ctx.obj["T8_USER"],
            t8_password=ctx.obj["T8_PASSWORD"]
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
def get_spectrum_command(ctx, machine, point, pmode, time):
    try:
        spectrum = get_spectrum(
            t8_host=ctx.obj["T8_HOST"],
            machine=machine,
            point=point,
            pmode=pmode,
            time=time,
            t8_user=ctx.obj["T8_USER"],
            t8_password=ctx.obj["T8_PASSWORD"]
        )[0]
        spectrum_data = list(spectrum) 

        if not spectrum_data:
            print("No data found in spectrum.")
            return
        else:
            print(f"Spectrum Data: {spectrum_data[:10]}...")    
    except Exception as e:
        print(f"Error retrieving spectrum: {e}")


@main.command(
    name="plot-wave",
    help="Plot the waveform data for a given machine, point, processing mode, and time.",
)
@pmode_params
@click.option("-t", "--time", required=True, help="Time of the wave (ISO format)")
@click.pass_context
def plot_wave(ctx, machine, point, pmode, time):
    try:

        waveform, sample_rate = get_wave(
            t8_host=ctx.obj["T8_HOST"],
            machine=machine,
            point=point,
            pmode=pmode,
            time=time,
            t8_user=ctx.obj["T8_USER"],
            t8_password=ctx.obj["T8_PASSWORD"]
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
    help="Plot the spectrum data for a given machine, point, processing mode, and time.",
)
@pmode_params
@click.option("-t", "--time", required=True, help="Time of the spectrum (ISO format)")
@click.pass_context
def plot_spectrum(ctx, machine, point, pmode, time):
    try:
        spectrum = get_spectrum(
            t8_host=ctx.obj["T8_HOST"],
            machine=machine,
            point=point,
            pmode=pmode,
            time=time,
            t8_user=ctx.obj["T8_USER"],
            t8_password=ctx.obj["T8_PASSWORD"]
        )[0]

        spectrum_data = list(spectrum) 
        if not spectrum_data:
            print("No data found in spectrum.")
            return
        else:
            print(f"Spectrum Data: {spectrum_data[:10]}...")  

        # Graficar el espectro
        plt.figure(figsize=(10, 6))
        plt.plot(spectrum_data)
        plt.title(f"Spectrum - {machine} - {point} - {pmode} - {time}")
        plt.xlabel("Frequency")
        plt.ylabel("Amplitude")
        plt.grid(True)
        plt.show()

    except Exception as e:
        print(f"Error retrieving spectrum: {e}")



# Ejecutar el CLI
if __name__ == "__main__":
    main()

