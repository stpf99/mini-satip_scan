#!/usr/bin/env python3

import os
import subprocess
import time
import re

# Plik konfiguracyjny z częstotliwościami
CONFIG_FILE = "channels.conf"

# Adres IP serwera SAT>IP
SERVER_IP = "192.168.1.1"

# Plik wyjściowy dla listy M3U
OUTPUT_FILE = "dvbt.conf"

# Czas oczekiwania między skanowaniami (w sekundach)
SLEEP_TIME = 10

# Sprawdzenie, czy plik konfiguracyjny istnieje
if not os.path.isfile(CONFIG_FILE):
    print(f"Błąd: Plik {CONFIG_FILE} nie istnieje!")
    exit(1)

# Sprawdzenie, czy octoscan istnieje i jest wykonywalny
if not os.access("./octoscan", os.X_OK):
    print("Błąd: Program octoscan nie istnieje lub nie jest wykonywalny!")
    exit(1)

# Inicjalizacja pliku wyjściowego (nadpisywanie)
with open(OUTPUT_FILE, "w") as f:
    f.write("#EXTM3U\n")

# Funkcja mapująca parametry z pliku na argumenty octoscan
def scan_frequency(channel_data):
    delivery_system = channel_data.get("DELIVERY_SYSTEM")
    frequency = int(channel_data.get("FREQUENCY"))
    bandwidth = int(channel_data.get("BANDWIDTH_HZ"))
    modulation = channel_data.get("MODULATION")
    transmission_mode = channel_data.get("TRANSMISSION_MODE")
    guard_interval = channel_data.get("GUARD_INTERVAL")
    code_rate_hp = channel_data.get("CODE_RATE_HP")

    # Konwersja częstotliwości z Hz na MHz
    freq_mhz = frequency / 1000000

    # Mapowanie parametrów na format octoscan
    if delivery_system == "DVBT":
        msys = "dvbt"
    elif delivery_system == "DVBT2":
        msys = "dvbt2"
    else:
        print(f"Nieznany system: {delivery_system}, pomijam.")
        return

    if bandwidth == 7000000:
        bw = "7"
    elif bandwidth == 8000000:
        bw = "8"
    else:
        print(f"Nieobsługiwana szerokość pasma: {bandwidth}, ustawiam domyślnie 8 MHz.")
        bw = "8"

    if transmission_mode == "8K":
        tmode = "8k"
    else:
        print(f"Nieobsługiwany tryb transmisji: {transmission_mode}, ustawiam domyślnie 8k.")
        tmode = "8k"

    if guard_interval == "1/4":
        gi = "1/4"
    else:
        print(f"Nieobsługiwany guard interval: {guard_interval}, ustawiam domyślnie 1/4.")
        gi = "1/4"

    # Wywołanie octoscan z odpowiednimi parametrami
    print("---------------------------------------------------------")
    print(f"Skanowanie: {delivery_system}, Freq={freq_mhz} MHz, BW={bw} MHz, TMODE={tmode}, GI={gi}")
    command = [
        "./octoscan",
        "--use_nit",
        f"--freq={freq_mhz}",
        f"--msys={msys}",
        f"--bw={bw}",
        f"--tmode={tmode}",
        f"--gi={gi}",
        SERVER_IP,
        "--append",
        OUTPUT_FILE
    ]
    print(f"Wykonuję: {' '.join(command)}")
    
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Logi błędów:")
            print(result.stderr)
        if result.returncode == 0:
            print("Skanowanie zakończone sukcesem.")
        else:
            print(f"Błąd: Skanowanie zakończone z kodem błędu {result.returncode}.")
    except subprocess.SubprocessError as e:
        print(f"Błąd podczas uruchamiania octoscan: {e}")

    # Sprawdzenie ostatnich linii pliku wyjściowego
    with open(OUTPUT_FILE, "r") as f:
        lines = f.readlines()
        last_lines = lines[-5:] if len(lines) > 5 else lines
        print(f"Ostatnie linie pliku {OUTPUT_FILE}:")
        print("".join(last_lines).strip())

    # Oczekiwanie przed kolejnym skanowaniem
    print(f"Czekam {SLEEP_TIME} sekund przed następnym skanowaniem...")
    time.sleep(SLEEP_TIME)
    print("---------------------------------------------------------")

# Parsowanie pliku konfiguracyjnego
channel_data = {}
with open(CONFIG_FILE, "r") as f:
    for line in f:
        line = line.strip()
        if line.startswith("#") or not line:
            continue
        if line == "[CHANNEL]":
            if channel_data:
                scan_frequency(channel_data)
                channel_data = {}
            continue
        match = re.match(r"(\w+)\s*=\s*(.+)", line)
        if match:
            key, value = match.groups()
            channel_data[key] = value

# Przetworzenie ostatniego kanału
if channel_data:
    scan_frequency(channel_data)

print(f"Skanowanie wszystkich częstotliwości zakończone. Wyniki zapisano w {OUTPUT_FILE}.")
