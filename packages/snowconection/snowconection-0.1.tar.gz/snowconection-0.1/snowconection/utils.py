import os
import json
import snowflake.connector
import re
from colorama import init, Fore, Style
from datetime import datetime

def load_snowflake_credentials():
    try:
        # Obtener la ruta de la carpeta raíz del proyecto
        root_dir = os.path.dirname(os.path.abspath(__file__))  # Esto obtiene el directorio del archivo actual (raíz del proyecto)
        creds_path = os.path.join(root_dir, 'snowflake_credentials.json')
        
        print(Fore.GREEN + f"Loading Snowflake credentials from: {creds_path}")
        
        with open(creds_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(Fore.RED + f"Issue with Snowflake credentials: {e}")
        raise

def connect_to_snowflake():
    creds = load_snowflake_credentials()
    print(Fore.GREEN + "Connecting to Snowflake credentials...")
    try:
        return snowflake.connector.connect(
            user=creds['user'],
            password=creds['password'],
            account=creds['account'],
            warehouse=creds['warehouse'],
            database=creds['database'],
            schema=creds['schema']
        )
    except Exception as e:
        print(Fore.RED + f"Cannot connect to Snowflake: {e}")
        raise
    
if __name__ == "__main__":
    init(autoreset=True)  # Inicia Colorama
    print(Fore.CYAN + "Starting Snowflake connection process...")

    # Intentar conectar a Snowflake
    try:
        conn = connect_to_snowflake()
        print(Fore.GREEN + "Connected successfully!")
        # Aquí puedes agregar más lógica si deseas interactuar con Snowflake
        conn.close()
    except Exception as e:
        print(Fore.RED + f"Error: {e}")