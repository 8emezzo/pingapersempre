import os



# ----------------------------------------------------------------------------------------------------- #
# Ineserisci i dati dei ping che vuoi monitorare:
# Destinazione e Zona li puoi mettere a piacere, servono solo per la visualizzazione.

ELENCO_IP_DA_MONITORARE = [
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






# -------------------------------------------------------------------------------------------------------- #
# Inserisci i secondi di storico del file CSV che vuoi analizzare durante il runtime di pingapersempre.bat
# Se metti 0 considera tutto il file CSV.

SECONDI_ANALISI_RUNTIME = 600 # 10 minuti circa





# -------------------------------------------------------------------------------------------------------- #
# Inserisci le ore di storico del file CSV che vuoi analizzare quando lanci statistiche.bat
# Se metti 0 considera tutto il file CSV.

ORE_DA_ANALIZZARE_NEL_CSV = 10







# -------------------------------------------------------------------------------------------------------- #
# Attenzione -> devi mettere >0 almeno una di queste due pause qua sotto, altrimenti va tutto a puttane

# Secondi di pausa tra un ping e l'altro dell'ELENCO_IP_DA_MONITORARE.
SECONDI_PAUSA_TRA_PING  = 1

# Secondi di pausa tra un ciclo di ping dell'ELENCO_IP_DA_MONITORARE.
SECONDI_PAUSA_TRA_CICLI = 3






# -------------------------------------------------------------------------------------------------------- #
# Secondi di timeout del singolo ping.
SECONDI_PING_TIMEOUT = 2






# -------------------------------------------------------------------------------------------------------- #
# Cambia i parametri di seguito solo se sai cosa stai facendo
# -------------------------------------------------------------------------------------------------------- #

#PC_NAME = os.environ['COMPUTERNAME']
#CSV_FILE = f"pingapersempre_{PC_NAME}.csv"

# Nome del file CSV
FILE_CSV = f"pingapersempre.csv"

# crea la cartella statistiche se non esiste
if not os.path.exists("statistiche"):
    os.makedirs("statistiche")

PATH_STATISTICHE = "statistiche"
FILE_HTML_STATISTICHE = f"{PATH_STATISTICHE}\\pingapersempre.html"

# Righe che carica dal file CSV per il runtime
MAX_LINES = int(SECONDI_ANALISI_RUNTIME / (SECONDI_PAUSA_TRA_PING + SECONDI_PAUSA_TRA_CICLI/len(ELENCO_IP_DA_MONITORARE)))


