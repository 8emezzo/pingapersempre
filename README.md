# pingapersempre

## Descrizione
Monitora nel tempo il ping su un elenco di IP

## Requisiti
Assicurati di avere installato Python nella macchina. Funziona su Windows ITA o EN, ma eventualmente con poche modifiche si può adattare ad altri sistemi operativi e/o lingue.

## Installazione
```
install.bat -> da eseguire solo la prima volta per installare le librerie Phython necessarie
```

## Utilizzo
```
pingapersempre.bat -> quando è in esecuzione salva l'esito dei ping in un file CSV
statistiche.bat    -> eseguire a piacimento per analizzare parte o tutto il file CSV
```

## Struttura del programma

```
pingapersempre/
│-- config.py          # Unico file di configurazione dove inserire i propri parametri
│-- pingapersempre.csv # file CSV con l'archivio dell'esito dei ping
│-- requirements.txt   # Librerie Python installate con install.bat
│-- main.py            # File py principale
│-- statistiche.py     # File py statistiche
│-- README.md          # Questo file
```

## Contatti
Per domande o suggerimenti, contattami a simoneventurin@gmail.com

## Licenza
Questo progetto è distribuito sotto la licenza MIAO LOL
(Modello Indipendente di Autorizzazione Open - Licenza Operativa Libera)

