import os



# ----------------------------------------------------------------------------------------------------- #
# Ineserisci i dati dei ping che vuoi monitorare:
# Destinazione e Zona li puoi mettere a piacere, servono solo per la visualizzazione.

elenco_ip_da_monitorare = [
     {"Destinazione": "Google DNS"      , "Zona": "US", "IP": "8.8.8.8"     }
    ,{"Destinazione": "Farm DNS"        , "Zona": "MI", "IP": "10.15.4.3"   }
    ,{"Destinazione": "Sito INPS"       , "Zona": "RM", "IP": "151.101.3.10"}
    ,{"Destinazione": "Router Belluno"  , "Zona": "BL", "IP": "10.112.255.1"}
    ,{"Destinazione": "Router Feltre"   , "Zona": "BL", "IP": "10.112.240.1"}
    ,{"Destinazione": "Router Pieve"    , "Zona": "BL", "IP": "10.112.230.1"}
    ,{"Destinazione": "Router Agordo"   , "Zona": "BL", "IP": "10.112.250.1"}
    ,{"Destinazione": "Router Sedico"   , "Zona": "BL", "IP": "10.112.200.1"}
    ,{"Destinazione": "Router Puos"     , "Zona": "BL", "IP": "10.112.210.1"}
    ,{"Destinazione": "Router Cortina"  , "Zona": "BL", "IP": "10.112.220.1"}
    ,{"Destinazione": "Router S.Stefano", "Zona": "BL", "IP": "10.112.190.1"}
]






# ----------------------------------------------------------------------------------------------------- #
# Inserisci il numero di ore nel passato che vuoi analizzare nel file CSV quando lanci le statistiche.
# Se metti 0 considera tutto il file CSV.

ORE_DA_ANALIZZARE_NEL_CSV = 10





# ----------------------------------------------------------------------------------------------------- #
# Inserisci i secondi di storico del file CSV che vuoi analizzare in runtime.
# Se metti 0 considera tutto il file CSV.

SECONDI_ANALISI_RUNTIME = 600 # 10 minuti circa





# ----------------------------------------------------------------------------------------------------- #
# Secondi di pausa tra un ping e l'altro dell'elenco_ip_da_monitorare.
SECONDI_PAUSA_TRA_PING  = 1

# Secondi di pausa tra un ciclo di ping dell'elenco_ip_da_monitorare.
SECONDI_PAUSA_TRA_CICLI = 3

# Attenzione -> devi mettere >0 almeno una di queste due pause qua sopra, altrimenti va tutto a puttane.






# ----------------------------------------------------------------------------------------------------- #
# Secondi di timeout del singolo ping.
SECONDI_PING_TIMEOUT = 2






# ----------------------------------------------------------------------------------------------------- #
# Cambia i parametri di seguito solo se sai cosa stai facendo.

PC_NAME = os.environ['COMPUTERNAME']

# Nome del file CSV
CSV_FILE = f"pingapersempre_{PC_NAME}.csv"
#CSV_FILE = f"pingapersempre.csv"

# Righe che carica dal file CSV per il runtime
MAX_LINES = int(SECONDI_ANALISI_RUNTIME / (SECONDI_PAUSA_TRA_PING + SECONDI_PAUSA_TRA_CICLI/len(elenco_ip_da_monitorare)))