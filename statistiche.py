from config import *

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

### CSV_FILE = "pingapersempre_BLCAAFBL00.csv"



# Carica il CSV in un DataFrame e imposta Timestamp come indice
df = pd.read_csv(CSV_FILE, parse_dates=["Timestamp"], index_col="Timestamp")

# taglia il dataframe nelle ultime ore
if ORE_DA_ANALIZZARE_NEL_CSV > 0:
    df = df[df.index > df.index.max() - pd.Timedelta(hours=ORE_DA_ANALIZZARE_NEL_CSV)]

df["Hour"] = df.index.hour
df["Day"] = df.index.date

df['Day_Hour'] = df['Day'].astype(str) + " " + df['Hour'].astype(str) + ":00"


n_ping = len(df)
n_ping_ok = int(df["Esito"].sum())
n_ping_ko = n_ping - n_ping_ok


# Statistiche generali

report = {
    "Numero totale di ping    ": int(n_ping),
    "Numero di ping riusciti  ": int(n_ping_ok),
    "Numero di ping falliti   ": int(n_ping_ko),
    "Percentuale di successo  ": f"{round((n_ping_ok / n_ping) * 100,2)} %",
    "Percentuale di fallimento": f"{round(((n_ping - n_ping_ok) / n_ping) * 100,2)} %",
    "Durata media             ": f"{int(df["Durata"].mean())} ms",
    "Durata massima           ": f"{int(df["Durata"].max())} ms",
    "Durata minima            ": f"{int(df["Durata"].min())} ms",
}

for key, value in report.items():
    print(f"{key}: {value}")

df_ko = df[df["Esito"] == 0]



# Ogni riga corrisponde a un ping perso, quindi raggruppo per destinazione, giorno e ora
ping_persi = df_ko.groupby(['Destinazione', 'Day', 'Hour']).size().reset_index(name='count')

if ping_persi.empty:
    print("Nessun ping perso")
else:

    # Tabella pivot:
    #    - righe: destinazione
    #    - colonne: combinazione giorno-ora
    #    - valori: numero di ping persi
    ping_persi['Day_Hour'] = ping_persi['Day'].astype(str) + " " + ping_persi['Hour'].astype(str) + ":00"
    heat_data = ping_persi.pivot(index='Destinazione', columns='Day_Hour', values='count').fillna(0)


    # Tracciamo la heatmap:
    plt.figure(figsize=(12, 6))  # regola le dimensioni in base alle esigenze
    sns.heatmap(
        heat_data, 
        annot=True,       # mostra i valori numerici nelle celle
        cmap='YlOrRd',    # puoi cambiare palette, ad esempio "Blues", "Greens", ecc.
        fmt='.0f',        # format dei numeri (interi)
        linewidths=0.5,   # bordo tra le celle
        cbar=True         # mostra la barra dei colori
    )
    plt.title('Mappa di calore dei ping persi (giorno e ora vs destinazione)')
    plt.xlabel('Giorno e Ora')
    plt.ylabel('Destinazione')
    plt.xticks(rotation=45, ha='right')  # Ruota le etichette dell'asse x
    plt.tight_layout()
    plt.show()


##############################
# STATISTICHE PER DESTINAZIONE
##############################

# statistiche di base per ogni destinazione
stats_per_destinazione = df.groupby("Destinazione").agg({
    "Durata": ["mean", "min", "max", "std"],
    "TTL": ["mean", "min", "max"],
    "Esito": ["count", "sum"]
})

# Per comodità, rinomino le colonne
stats_per_destinazione.columns = [
    "Durata_media", "Durata_min", "Durata_max", "Durata_std",
    "TTL_medio", "TTL_min", "TTL_max",
    "Ping_totali", "Ping_riusciti",
]
stats_per_destinazione["Ping_falliti"] = stats_per_destinazione["Ping_totali"] - stats_per_destinazione["Ping_riusciti"]
stats_per_destinazione["Percentuale_fallimento"] = 100 -(stats_per_destinazione["Ping_riusciti"] / stats_per_destinazione["Ping_totali"] * 100).round(2)
stats_per_destinazione["Percentuale_fallimento"] = stats_per_destinazione["Percentuale_fallimento"].round(2)
stats_per_destinazione["Durata_media"] = stats_per_destinazione["Durata_media"].round(1)
stats_per_destinazione["Durata_std"] = stats_per_destinazione["Durata_std"].round(1)
stats_per_destinazione["TTL_medio"] = stats_per_destinazione["TTL_medio"].astype(int)



print("\nStatistiche per destinazione:")
print(stats_per_destinazione)



plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x="Destinazione", y="Durata")
plt.xticks(rotation=45)
plt.title("Distribuzione durata ms per destinazione")
plt.ylabel("Durata (ms)")
plt.xlabel("Destinazione")
plt.tight_layout()
plt.show()



#########################################
# STATISTICHE PER DATA/ORA e DESTINAZIONE
#########################################

stats_per_data_dest = df.groupby(["Day_Hour", "Destinazione"]).agg({
    "Durata": ["mean", "min", "max"],
      "Esito": ["count", "sum"]
})


# Per comodità rinomino le colonne
stats_per_data_dest.columns = [
    "Durata_media", "Durata_min", "Durata_max", 
    "Ping_totali", "Ping_riusciti",
]

stats_per_data_dest["Ping_falliti"] = stats_per_data_dest["Ping_totali"] - stats_per_data_dest["Ping_riusciti"]
stats_per_data_dest["Percentuale_fallimento"] = 100 -(stats_per_data_dest["Ping_riusciti"] / stats_per_data_dest["Ping_totali"] * 100).round(2)
stats_per_data_dest["Percentuale_fallimento"] = stats_per_data_dest["Percentuale_fallimento"].round(2)
stats_per_data_dest["Durata_media"] = stats_per_data_dest["Durata_media"].round(1)


print("\nStatistiche per data e destinazione:")
print(stats_per_data_dest)














#  DataFrame di appoggio, raggruppando per (timestamp, destinazione).
df_line = (
    df.groupby(["Timestamp", "Destinazione"])["Durata"]
      .mean()  # media dei tempi di ping
      .reset_index()
)

# Grafico con seaborn
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_line, x="Timestamp", y="Durata", hue="Destinazione")
plt.xlabel("Data/ora")
plt.ylabel("Durata media (ms)")
plt.title("Evoluzione della durata media per destinazione nel tempo")
plt.legend(title="Destinazione", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()
plt.show()








# grafico per ogni destinazione
destinations = df['Destinazione'].unique()

for destination in destinations:
    df_dest = df[df['Destinazione'] == destination]
    # Grafico con seaborn
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_dest, x="Timestamp", y="Durata", hue="Destinazione")
    plt.xlabel("Data/ora")
    plt.ylabel("Durata media (ms)")
    plt.title("Evoluzione della durata media per destinazione nel tempo")
    plt.legend(title="Destinazione", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.tight_layout()
    plt.show()



# medio timestamp al più vicino intervallo di 10 minuti
df["Timestamp_10min"] = pd.to_datetime(df.index).floor("10min")

# Creiamo il DataFrame aggregato
df_line = (
    df.groupby(["Timestamp_10min", "Destinazione"])["Durata"]
      .mean()  # Media dei tempi di ping ogni 5 minuti
      .reset_index()
)

# Grafico
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_line, x="Timestamp_10min", y="Durata", hue="Destinazione")
plt.xlabel("Data/ora (aggregata ogni 10 minuti)")
plt.ylabel("Durata media (ms)")
plt.title("(MEDIA 10 min) Evoluzione della durata media per destinazione nel tempo ")
plt.legend(title="Destinazione", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


















plt.figure(figsize=(10, 6))
sns.histplot(data=df, x="Durata", bins=30, kde=True)
plt.xlabel("Durata (ms)")
plt.ylabel("Frequenza")
plt.title("Distribuzione dei tempi di risposta (ms)")
plt.show()

