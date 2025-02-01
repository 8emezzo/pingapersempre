# pingapersempre

## Descrizione
Monitora nel tempo il ping di un elenco di IP. Salva l'esito dei ping nel file pingapersempre.csv e aggiorna le statistiche nel file ./statistiche/index.html

## Requisiti
Assicurati di avere installato Python nella macchina. Funziona su Windows (lingua ITA o EN), ma con poche modifiche si può adattare in modo che supporti qualsiasi sistema operativo e/o lingua.

## Installazione
```
install.bat
```

## Configurazione
```
Editare il file config.py ed inserire i propri dati
```

## Utilizzo
```
pingapersempre.bat
```

## Struttura del programma

```
pingapersempre/
│-- config.py          # file di configurazione
│-- main.py            # File py principale
│-- statistiche.py     # File py statistiche
│-- pingapersempre.csv # file CSV con l'archivio dell'esito dei ping (creato alla prima esecuzione)
│-- requirements.txt   # elenco librerie Python
│-- install.bat        # installa le librerie Python contenute in requirements.txt
│-- pingapersempre.bat # Lancia il programma
│-- statistiche.bat    # Forza l'aggiornamento del file HTML delle statistiche
│-- README.md          # Questo file
│-- statistiche/       # Sottocartella contenente i file delle statistiche
    │-- index.html      # File HTML con le statistiche (generato dal programma)
```

## Contatti
Per domande o suggerimenti, contattami a simoneventurin@gmail.com

## Licenza
Questo progetto è distribuito sotto la licenza MIAO LOL
(Modello Indipendente di Autorizzazione Open - Licenza Operativa Libera)

