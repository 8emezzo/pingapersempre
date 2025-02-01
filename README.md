# pingapersempre

## Descrizione
Monitora nel tempo il ping di un elenco di IP.
```
Salva l'esito dei ping nel file pingapersempre.csv e ciclicamente aggiorna il file statistiche.html
```

## Requisiti
Assicurati di avere installato Python nella macchina.
```
Funziona su Windows, lingua ITA o EN.
Con poche modifiche si può adattare in modo che supporti qualsiasi sistema operativo e/o lingua.
(sia chiaro, modifiche che non ho nessuna intenzione di fare)
```

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
│-- main.py            # file py principale
│-- statistiche.py     # file py statistiche
│-- pingapersempre.csv # file CSV con l'archivio dell'esito dei ping (creato alla prima esecuzione)
│-- requirements.txt   # elenco librerie Python
│-- install.bat        # installa le librerie Python contenute in requirements.txt
│-- pingapersempre.bat # lancia il programma
│-- statistiche.bat    # forza l'aggiornamento del file HTML delle statistiche
│-- statistiche.html   # file HTML con le statistiche
│-- README.md          # questo file
```

## Contatti
```
Per domande o suggerimenti, contattami a simoneventurin@gmail.com
```

## Licenza
```
Questo progetto è distribuito sotto la licenza MIAO LOL
(Modello Indipendente Antani Open - Licenza Operativa Libera)
```

