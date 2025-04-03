# t8-client

**t8-client** es una aplicación de línea de comandos que permite interactuar con la API de T8 para obtener datos como formas de onda y espectros, y realizar acciones como visualizarlos, guardarlos en CSV y representarlos gráficamente.

## Descripción del Proyecto

El objetivo de este proyecto es crear una aplicación que se conecte a la API del T8 y realice diversas acciones utilizando subcomandos. Los subcomandos incluyen la obtención de datos, su visualización y la conversión de la fecha.

## Requisitos

- Python 3.8 o superior
- `poetry` para la gestión de dependencias

## Instalación

1. Crea un nuevo proyecto utilizando `poetry`:

    ```bash
    poetry new t8-client
    cd t8-client
    ```

2. Agrega las dependencias necesarias para el proyecto, como `click`, `requests`, entre otras. Puedes hacer esto manualmente o utilizando `poetry add` para cada una. Ejemplo:

    ```bash
    poetry add click requests matplotlib
    ```

3. Instala las dependencias del proyecto ejecutando:

    ```bash
    poetry install
    ```

4. Verifica que la instalación fue correcta ejecutando el siguiente comando:

    ```bash
    poetry run t8-client --help
    ```

## Configuración de las Credenciales

El proyecto utiliza las siguientes variables de entorno para acceder a la API de T8:

- **T8_HOST**: La URL base de la API 
- **T8_USER**: El nombre de usuario para autenticarte en la API.
- **T8_PASSWORD**: La contraseña para autenticarte en la API.


## Usando el archivo `.env` 

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

T8_HOST=https://lzfs45.mirror.twave.io/lzfs45
T8_USER=tu_usuario
T8_PASSWORD=tu_contraseña

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



