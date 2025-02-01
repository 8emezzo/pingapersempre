from config import *

import os
import io
import time
import csv
import re

import subprocess
import threading
import webbrowser

from collections import deque
from datetime import datetime

import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd




# Variabile globale per la sincronizzazione tra thread
lock = threading.Lock()




def genera_statistiche(open_browser=False, secondi_pausa_iniziale=SECONDI_AGGIORNAMENTO_HTML):

    # Pausa iniziale
    time.sleep(secondi_pausa_iniziale)

    # Carica il CSV in un DataFrame e imposta Timestamp come indice
    df = pd.read_csv(FILE_CSV, parse_dates=["Timestamp"], index_col="Timestamp")

    # taglia il dataframe nelle ultime ore
    if ORE_DA_ANALIZZARE_NEL_CSV > 0:
        df = df[df.index > df.index.max() - pd.Timedelta(hours=ORE_DA_ANALIZZARE_NEL_CSV)]

    # aggiungo colonne utlili per le analisi
    df["Hour"] = df.index.hour
    df["Day"] = df.index.date
    df['Day_Hour'] = df['Day'].astype(str) + " " + df['Hour'].astype(str) + ":00"
    df['Zona_Destinazione'] = df['Zona'] + " - " + df['Destinazione']

    # df dei soli ping falliti
    df_ping_falliti = df[df["Esito"] == 0]

    # data minima e massima del df
    min_time_df = df.index.min()
    max_time_df = df.index.max()


    # ------------------------- #
    # Statistiche generali      #
    # ------------------------- #

    n_ping = len(df)
    n_ping_ok = int(df["Esito"].sum())
    n_ping_ko = n_ping - n_ping_ok

    report_statistiche_generali  = {
        "Percentuale di fallimento ": f"{round(((n_ping_ko) / n_ping) * 100,2)} %",
        "Numero ping totale        ": int(n_ping),
        "Numero ping falliti       ": int(n_ping_ko),
        "Numero ping riusciti      ": int(n_ping_ok),
        "Durata media ping         ": f"{int(df["Durata"].mean())} ms",
        "Dev. standard durata ping ": f"{int(df["Durata"].std())} ms",
    }


    for key, value in report_statistiche_generali.items():
        print(f"{key}: {value}")


    # ------------------------------- #
    # Statistiche per destinazione    #
    # ------------------------------- #

    # statistiche di base per ogni destinazione
    stats_per_destinazione = df.groupby("Zona_Destinazione").agg({
        "Esito": ["count", "sum"],
        "Durata": ["mean", "min", "max"],
        "TTL": ["mean", "min", "max"],
    })

    # Per comodità, rinomino le colonne
    stats_per_destinazione.columns = [
        "Ping_totali", "Ping_riusciti",
        "Durata_media", "Durata_min", "Durata_max",
        "TTL_medio", "TTL_min", "TTL_max",
    ]
    stats_per_destinazione["Ping_falliti"] = stats_per_destinazione["Ping_totali"] - stats_per_destinazione["Ping_riusciti"]
    stats_per_destinazione["% fallimento"] = 100 -(stats_per_destinazione["Ping_riusciti"] / stats_per_destinazione["Ping_totali"] * 100).round(2)
    stats_per_destinazione["% fallimento"] = stats_per_destinazione["% fallimento"].round(2)
    stats_per_destinazione["Durata_media"] = stats_per_destinazione["Durata_media"].astype(int)
    stats_per_destinazione["TTL_medio"] = stats_per_destinazione["TTL_medio"].astype(int)

    stats_per_destinazione.drop(columns=[ "Ping_riusciti"], inplace=True)

    stats_per_destinazione = stats_per_destinazione[["% fallimento", "Ping_totali", "Ping_falliti" ] + 
            [col for col in stats_per_destinazione.columns if col not in ["Ping_totali", "Ping_falliti", "% fallimento"]]]

    stats_per_destinazione = stats_per_destinazione.sort_values(by="% fallimento", ascending=False)

    print("\nStatistiche per destinazione:")
    print(stats_per_destinazione.to_string())


    # ----------------------------------------- #
    # Statistiche per giorno/ora e destinazione #
    # ----------------------------------------- #

    stats_per_data_dest = df.groupby(["Day_Hour", "Zona_Destinazione"]).agg({
        "Durata": ["mean", "min", "max"],
        "Esito": ["count", "sum"]
    })

    # Per comodità rinomino le colonne
    stats_per_data_dest.columns = [
        "Durata_media", "Durata_min", "Durata_max", 
        "Ping_totali", "Ping_riusciti",
    ]

    stats_per_data_dest["Ping_falliti"] = stats_per_data_dest["Ping_totali"] - stats_per_data_dest["Ping_riusciti"]
    stats_per_data_dest["% fallimento"] = 100 -(stats_per_data_dest["Ping_riusciti"] / stats_per_data_dest["Ping_totali"] * 100).round(2)
    stats_per_data_dest["% fallimento"] = stats_per_data_dest["% fallimento"].round(2)
    stats_per_data_dest["Durata_media"] = stats_per_data_dest["Durata_media"].round(1)

    stats_per_data_dest.drop(columns=[ "Ping_riusciti"], inplace=True)

    stats_per_data_dest = stats_per_data_dest.sort_values(by=["Day_Hour",  "% fallimento", "Zona_Destinazione"], ascending=[True, False, True])

    stats_per_data_dest = stats_per_data_dest[["% fallimento", "Ping_totali", "Ping_falliti" ] + 
            [col for col in stats_per_data_dest.columns if col not in ["Ping_totali", "Ping_falliti", "% fallimento"]]]

    print("\nStatistiche per data e destinazione:")
    print(stats_per_data_dest.to_string()) 


    # ------------------------------- #
    # Ping persi (mappa di calore)    #
    # ------------------------------- #

    # ping persi raggruppati per zona, destinazione, giorno e ora
    df_ping_falliti_raggruppati = df_ping_falliti.groupby(['Zona_Destinazione', 'Day_Hour']).size().reset_index(name='count')

    if df_ping_falliti_raggruppati.empty:
        print("Non stampo la mappa di calore dei ping persi perché non c'è nessun ping perso")

        # se non ci sono ping persi, stampo un png vuoto
        plt.figure(figsize=(12, 6))
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(f"{PATH_STATISTICHE}\\mappa_ping_persi.png")
        
    else:

        heat_data = df_ping_falliti_raggruppati.pivot(index='Zona_Destinazione', columns='Day_Hour', values='count').fillna(0)
        heat_data = heat_data.astype(int)
        # somma le righe per avere il totale dei ping persi per destinazione
        heat_data['Totale'] = heat_data.sum(axis=1)
        # ordina le righe per il totale dei ping persi decrescente
        heat_data = heat_data.sort_values(by='Totale', ascending=False)
        # plot mappa di calore
        plt.figure(figsize=(12, 6))

        sns.heatmap(
            data=heat_data.drop(columns='Totale'),
            annot=True,       # mostra i valori numerici nelle celle
            cmap='YlOrRd',    # puoi cambiare palette, ad esempio "Blues", "Greens", ecc.
            fmt='.0f',        # format dei numeri (interi)
            linewidths=0.5,   # bordo tra le celle
            cbar=True         # mostra la barra dei colori
        )
        
        plt.title('Mappa delle destinazioni che hanno perso ping nel periodo analizzato')
        plt.xlabel('Giorno/Ora')
        plt.ylabel('Destinazione')
        plt.xticks(rotation=45, ha='right')  # Ruota le etichette dell'asse x
        plt.tight_layout()
        #plt.show()
        plt.savefig(f"{PATH_STATISTICHE}\\mappa_ping_persi.png")


    # ------------------------------------ #
    # Distribuzione durata ping per zona   #
    # ------------------------------------- #
    df_distribuzione = df.sort_values("Zona_Destinazione")

    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df_distribuzione, x="Zona_Destinazione", y="Durata")
    plt.xticks(rotation=45)
    plt.title("Distribuzione durata ping per destinazione")
    plt.ylabel("Durata ping(ms)")
    plt.xlabel("Destinazione")
    plt.tight_layout()
    #plt.show()
    plt.savefig(f"{PATH_STATISTICHE}\\distribuzione_durata_ping_per_zona.png")


    # --------------------------------------- #
    # Evoluzione della durata ping nel tempo  #
    # --------------------------------------- #

    #  DataFrame di appoggio, raggruppando per (timestamp, destinazione).
    df_line = (
        df.groupby(["Timestamp", "Zona_Destinazione"])["Durata"]
        .mean()  # media dei tempi di ping
        .reset_index()
        .sort_values("Zona_Destinazione")
    )

    # Grafico con seaborn
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_line, x="Timestamp", y="Durata", hue="Zona_Destinazione")
    plt.xlabel("Data/ora")
    plt.ylabel("Durata media (ms)")
    plt.title("Evoluzione della durata media per destinazione nel tempo")
    plt.legend(title="Destinazione", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.tight_layout()
    #plt.show()
    plt.savefig(f"{PATH_STATISTICHE}\\evoluzione_durata_ping_nel_tempo.png")


    # ----------------------------------------------------------- #
    # Evoluzione della durata pingnel tempo per ogni destinazione #
    # ----------------------------------------------------------- #

    # grafico per ogni destinazione
    destinations = df['Zona_Destinazione'].unique()

    for destination in destinations:
        df_dest = df[df['Zona_Destinazione'] == destination]
        # Grafico con seaborn
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=df_dest, x="Timestamp", y="Durata", hue="Zona_Destinazione")
        plt.xlabel("Data/ora")
        plt.ylabel("Durata media (ms)")
        plt.title("Evoluzione della durata ping media per destinazione nel tempo")
        plt.legend(title="Destinazione", bbox_to_anchor=(1.02, 1), loc="upper left")
        plt.tight_layout()
        #plt.show()
        plt.savefig(f"{PATH_STATISTICHE}\\evoluzione_durata_ping_nel_tempo_per_destinazione_{destination}.png")


    # --------------------------------------------------------------------------- #
    # Evoluzione della durata ping nel tempo per ogni destinazione (media 10 min) #
    # --------------------------------------------------------------------------- #

    # medio timestamp al più vicino intervallo di 10 minuti
    df["Timestamp_10min"] = pd.to_datetime(df.index).floor("10min")

    # Creiamo il DataFrame aggregato
    df_line = (
        df.groupby(["Timestamp_10min", "Zona_Destinazione"])["Durata"]
        .mean()  # Media dei tempi di ping ogni 5 minuti
        .reset_index()
        .sort_values("Zona_Destinazione")
    )

    # Grafico
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_line, x="Timestamp_10min", y="Durata", hue="Zona_Destinazione")
    plt.xlabel("Data/ora (aggregata ogni 10 minuti)")
    plt.ylabel("Durata media (ms)")
    plt.title("(MEDIA 10 min) Evoluzione della durata ping media per destinazione nel tempo ")
    plt.legend(title="Destinazione", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.xticks(rotation=45)
    plt.tight_layout()
    #plt.show()
    plt.savefig(f"{PATH_STATISTICHE}\\evoluzione_durata_ping_nel_tempo_per_destinazione_media_10_min.png")


    # ------------------------------- #
    # Distribuzione dei tempi di ping #
    # ------------------------------- #

    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x="Durata", bins=50, kde=True)
    plt.xlabel("Durata (ms)")
    plt.ylabel("Frequenza")
    plt.title("Distribuzione dei tempi di risposta (ms)")
    #plt.show()
    plt.savefig(f"{PATH_STATISTICHE}\\distribuzione_tempi_di_ping.png")

    with open(FILE_HTML_STATISTICHE, "w", encoding="utf-8") as f:
        # anche un minimo di css
        f.write("<style>table {border-collapse: collapse;} th, td {border: 1px solid black; padding: 5px;}</style>")

        f.write("<html><body>")
        f.write(f"<h1>Statistiche dei ping eseguiti nelle ultime {ORE_DA_ANALIZZARE_NEL_CSV} ore, salvate nel file CSV, dal {min_time_df} fino al {max_time_df}</h1>")
        f.write("<table>")
        for key, value in report_statistiche_generali.items():
            f.write(f"<tr><td>{key}</td><td>{value}</td></tr>")
        f.write("</table>")

        f.write("<h1>Mappa di calore dei ping persi</h1>")
        f.write(f"<img src='{PATH_STATISTICHE}\\mappa_ping_persi.png'>")

        f.write("<h1>Statistiche per destinazione</h1>")
        f.write(stats_per_destinazione.to_html())

        f.write("<h1>Distribuzione durata ping per zona</h1>")
        f.write(f"<img src='{PATH_STATISTICHE}\\distribuzione_durata_ping_per_zona.png'>")

        f.write("<h1>Evoluzione della durata ping nel tempo di tutte le destinazioni</h1>")
        f.write(f"<img src='{PATH_STATISTICHE}\\evoluzione_durata_ping_nel_tempo.png'>")
        
        f.write("<h1>Media a 10 minuti dell'evoluzione della durata ping nel tempo per ogni destinazione</h1>")
        f.write(f"<img src='{PATH_STATISTICHE}\\evoluzione_durata_ping_nel_tempo_per_destinazione_media_10_min.png'>")

        f.write("<hr>") #linea di separazione
        for destination in destinations:
            f.write(f"<h1>Evoluzione della durata ping nel tempo per la destinazione {destination}</h1>")
            f.write(f"<img src='{PATH_STATISTICHE}\\evoluzione_durata_ping_nel_tempo_per_destinazione_{destination}.png'>")
        f.write("<hr>") #linea di separazione

        f.write("<h1>Distribuzione dei tempi di ping</h1>")
        f.write(f"<img src='{PATH_STATISTICHE}\\distribuzione_tempi_di_ping.png'>")

        f.write("<h1>Statistiche per data/ora e destinazione</h1>")
        f.write(stats_per_data_dest.to_html())

        #fine html
        f.write("</body></html>")

    if open_browser:
        # apre il file HTML con il browser predefinito
        webbrowser.open(FILE_HTML_STATISTICHE)



def file_CSV():
    # Creazione intestazione CSV se il file non esiste
    if not os.path.exists(FILE_CSV):
        with open(FILE_CSV, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Esito",  "Durata", "Destinazione", "IP", "Zona", "TTL", "Timestamp"])




def esegui_ping_infiniti():
    # Esegue il ping per ogni IP e registra i risultati in un CSV

    while True:
        with open(FILE_CSV, mode='a', newline='') as file:
            writer = csv.writer(file)
            
            for entry in ELENCO_IP_DA_MONITORARE:
                timestamp    = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ip           = entry['IP']
                destinazione = entry["Destinazione"]
                zona         = entry["Zona"]
                ping_output  = subprocess.run(["ping", "-n", "1", "-w", str(SECONDI_PING_TIMEOUT * 1000), ip ], capture_output=True, text=True)
                esito        = int("TTL=" in ping_output.stdout)

                # Estrae durata e TTL
                durata_match = re.search(r'(?:durata|time)[=<]?(\d+)ms', ping_output.stdout)
                ttl_match    = re.search(r'TTL=(\d+)', ping_output.stdout)
                durata       = int(durata_match.group(1)) if durata_match else SECONDI_PING_TIMEOUT * 1000
                ttl          = int(ttl_match.group(1)) if ttl_match else -1

                with lock:
                    writer.writerow([esito, durata, destinazione, ip, zona, ttl, timestamp])
                
                time.sleep(SECONDI_PAUSA_TRA_PING)

        time.sleep(SECONDI_PAUSA_TRA_CICLI)



def output_runtime():
    # Aggiorna la schermata con i risultati in tempo reale

    while True:
        os.system('cls')

        # Legge solo le ultime MAX_LINES
        with open(FILE_CSV, "r", encoding="utf-8") as f:
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
        agg_df = df.groupby(["Zona", "Destinazione", "IP"]).agg(
            Durata_media=("Durata", "mean"),
            TTL_medio=("TTL", "mean"),
            Ping_totali=("Esito", "count"),
            Ping_falliti=("Esito", lambda x: (x == 0).sum())
        ).round().astype(int).reset_index()

        agg_df["% fallimenti"] = (agg_df["Ping_falliti"] / agg_df["Ping_totali"] * 100).round(2)

        # Ordina per % fallimenti decrescente, Zona crescente, Destinazione crescente
        agg_df = agg_df.sort_values(["% fallimenti", "Zona", "Destinazione"], ascending=[False, True, True])

        print("------------------------------------------------------------------------------------------------------")
        print(f"Statistiche ultimi {diff_time:.1f} minuti aggiornate al {max_time}")
        print("------------------------------------------------------------------------------------------------------")
        print(agg_df.to_string(index=False))
        print("------------------------------------------------------------------------------------------------------")
        time.sleep(5)



if __name__ == "__main__":

    file_CSV()  # Crea il file CSV se non esiste

    # Avvia i thread
    ping_thread = threading.Thread(target=esegui_ping_infiniti, daemon=True)
    ping_thread.start()


    if SECONDI_AGGIORNAMENTO_HTML > 0 :
        # Avvia il thread per la creazione delle statistiche
        stats_thread = threading.Thread(target=genera_statistiche, daemon=True)
        stats_thread.start()

    output_runtime()  # Funzione principale per l'aggiornamento dello schermo
