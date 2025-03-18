import argparse
import os

# Configurar argparse para recibir credenciales
def parse_args():
    parser = argparse.ArgumentParser(description="Configuración de las credenciales de acceso")
    parser.add_argument("--user", type=str, help="Nombre de usuario para la API")
    parser.add_argument("--password", type=str, help="Contraseña para la API")
    parser.add_argument("--host", type=str, help="Host para la API")
    return parser.parse_args()

# Uso de los argumentos
args = parse_args()

# Ahora puedes acceder a las credenciales
user = args.user
password = args.password
host = args.host

# Aquí puedes usar esas variables para conectarte a la API
print(f"Conectando con el usuario: {user} al host: {host}")
