from config import *

import os
import io
import time
import csv
import subprocess
import threading
import re

from datetime import datetime
from collections import deque

import pandas as pd


### CSV_FILE = "pingapersempre_BLCAAFBL00.csv"

# Creazione intestazione CSV se il file non esiste
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Esito",  "Durata", "Destinazione", "IP", "Territorio", "TTL", "Timestamp"])

# Variabile globale per la sincronizzazione tra thread
lock = threading.Lock()



def esegui_ping_infiniti():
    # Esegue il ping per ogni IP e registra i risultati in un CSV

    while True:
        with open(CSV_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            
            for entry in elenco_ip_da_monitorare:
                timestamp    = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ip           = entry['IP']
                destinazione = entry["Destinazione"]
                territorio   = entry["Territorio"]
                ping_output  = subprocess.run(["ping", "-n", "1", "-w", str(SECONDI_PING_TIMEOUT * 1000), ip ], capture_output=True, text=True)
                esito        = int("TTL=" in ping_output.stdout)

                # Estrae durata e TTL
                durata_match = re.search(r'(?:durata|time)[=<]?(\d+)ms', ping_output.stdout)
                ttl_match    = re.search(r'TTL=(\d+)', ping_output.stdout)
                durata       = int(durata_match.group(1)) if durata_match else SECONDI_PING_TIMEOUT * 1000
                ttl          = int(ttl_match.group(1)) if ttl_match else -1

                with lock:
                    writer.writerow([esito, durata, destinazione, ip, territorio, ttl, timestamp])
                
                time.sleep(SECONDI_PAUSA_TRA_PING)

        time.sleep(SECONDI_PAUSA_TRA_CICLI)



def output_runtime():
    # Aggiorna la schermata con i risultati in tempo reale

    while True:
        os.system('cls')

        # Legge solo le ultime MAX_LINES
        with open(CSV_FILE, "r", encoding="utf-8") as f:
            header = f.readline()  # Legge la prima riga (intestazione)
            if MAX_LINES == 0:
                last_lines = f.readlines()
            else:
                last_lines = deque(f, maxlen=MAX_LINES)  # Mantiene solo le ultime MAX_LINES righe in memoria

        df = pd.read_csv(io.StringIO(header + "".join(last_lines)))

        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        # calcola la data minima e massima e la differenza
        min_time = df['Timestamp'].min()
        max_time = df['Timestamp'].max()
        diff_time = (max_time - min_time).total_seconds() / 60

        # Raggruppa per Destinazione e IP, calcola media Durata e TTL, e contiamo gli Esito = 0
        agg_df = df.groupby(["Destinazione", "IP"]).agg(
            Durata_media=("Durata", "mean"),
            TTL_medio=("TTL", "mean"),
            Ping_totali=("Esito", "count"),
            Ping_falliti=("Esito", lambda x: (x == 0).sum())
        ).round().astype(int).reset_index()

        agg_df["% fallimenti"] = (agg_df["Ping_falliti"] / agg_df["Ping_totali"] * 100).round(2)


        print(f"Statistiche ultimi {diff_time:.1f} minuti, aggiornate al: {max_time}")
       
        print(agg_df.to_string(index=False))
        time.sleep(5)



if __name__ == "__main__":
    # Avvia i thread
    ping_thread = threading.Thread(target=esegui_ping_infiniti, daemon=True)
    ping_thread.start()

    output_runtime()  # Funzione principale per l'aggiornamento dello schermo
