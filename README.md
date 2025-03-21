# t8-client

**t8-client** es una aplicación de línea de comandos que permite interactuar con la API de T8 para obtener datos como formas de onda y espectros, y realizar acciones como visualizarlos, guardarlos en CSV y representarlos gráficamente.

## Descripción del Proyecto

El objetivo de este proyecto es crear una aplicación que se conecte a la API del T8 y realice diversas acciones utilizando subcomandos. Los subcomandos incluyen la obtención de datos, su visualización y la conversión de la fecha.


## Credenciales

El usuario, contraseña y host se leeran desde variables de entorno.

## Entry Point

El comando `t8-client` se define como el *entry point* del proyecto.


## Comandos

La aplicación `t8-client` incluye los siguientes subcomandos:

- **`list-waves`**: Lista las formas de onda disponibles para una máquina, punto y modo de procesamiento especificados.

    ```bash
    t8-client list-waves -M <máquina> -p <punto> -m <pmode>
    ```

- **`list-spectra`**: Lista los espectros disponibles para una máquina, punto y modo de procesamiento especificados.

    ```bash
    t8-client list-spectra -M <máquina> -p <punto> -m <pmode>
    ```

- **`get-wave`**: Obtiene la forma de onda, dados los parámetros `MACHINE`, `POINT`, `PMODE` y `DATE`.

    ```bash
    t8-client get-wave -M <máquina> -p <punto> -m <pmode> -t <fecha>
    ```

- **`get-spectrum`**: Obtiene el espectro, dados los parámetros `MACHINE`, `POINT`, `PMODE` y `DATE`.

    ```bash
    t8-client get-spectrum -M <máquina> -p <punto> -m <pmode> -t <fecha>
    ```

- **`plot-wave`**: Representa la forma de onda en una gráfica, dados los parámetros `MACHINE`, `POINT`, `PMODE` y `DATE`.

    ```bash
    t8-client plot-wave -M <máquina> -p <punto> -m <pmode> -t <fecha>
    ```

- **`plot-spectrum`**: Representa el espectro en una gráfica, dados los parámetros `MACHINE`, `POINT`, `PMODE` y `DATE`.

    ```bash
    t8-client plot-spectrum -M <máquina> -p <punto> -m <pmode> -t <fecha>
    ```

## Tests

Los tests se ejecutan mediante `pytest` para asegurar el correcto funcionamiento de la aplicación.



