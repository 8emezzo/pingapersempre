
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





# -------------------------------------------------------------------------------------------------------------------- #
# Inserisci i secondi ogni quanto vuoi aggiornare il file statistiche.html
# E' consigliato non mettere meno di 60 secondi, dato che la produzione del file HTML potrebbe appesantire la macchina
# Se metti 0 non produce mai il file. Eventualmente lo puoi produrre a parte con il comando statitiche.bat
SECONDI_AGGIORNAMENTO_FILE_HTML_STATISTICHE = 1800 # 30 minuti






# -------------------------------------------------------------------------------------------------------------------- #
# Inserisci le ore di storico del file CSV che vuoi analizzare nel file statistiche.html
# Se metti 0 considera tutto il file CSV.
ORE_DA_ANALIZZARE_NEL_CSV_PER_LE_STATISTICHE = 10






# -------------------------------------------------------------------------------------------------------------------- #
# Inserisci i secondi di storico del file CSV che vuoi analizzare durante il runtime di pingapersempre.bat
# Se metti 0 considera tutto il file CSV.
SECONDI_DA_ANALIZZARE_NEL_CSV_PER_IL_RUNTIME = 600 # 10 minuti





# -------------------------------------------------------------------------------------------------------------------- #
# Non mettere entrambi i due seguenti parametri a 0, altrimenti mi sa che va tutto a puttane
# Puoi mettere anche numeri in virgola mobile (es. 0.5)

# Secondi di pausa tra un ping e l'altro dell'ELENCO_IP_DA_MONITORARE. Accetta anche numeri con virgola (es. 0.5)
SECONDI_PAUSA_TRA_PING  = 1

# Secondi di pausa tra un ciclo di ping dell'ELENCO_IP_DA_MONITORARE. Accetta anche numeri con virgola (es. 1.5)
SECONDI_PAUSA_TRA_CICLI = 3






# -------------------------------------------------------------------------------------------------------------------- #
# Secondi di timeout del singolo ping. Accetta anche numeri con virgola (es. 1.5)
# Consigliato mettere almeno 1 secondo
SECONDI_PING_TIMEOUT = 2







# -------------------------------------------------------------------------------------------------------------------- #
# Nomi file/path
FILE_CSV              = "pingapersempre.csv"
FILE_HTML_STATISTICHE = "statistiche.html"
PATH_STATISTICHE      = "statitiche"
