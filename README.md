# pingapersempre

## Descrizione
Monitora nel tempo il ping di un elenco di IP

## Requisiti
Assicurati di avere installato Python nella macchina. Funziona su Windows (lingua ITA o EN), ma con poche modifiche si può adattare in modo che supporti qualsiasi sistema operativo e/o lingua.

## Installazione
```
install.bat -> Da eseguire solo la prima volta per installare le librerie Phython necessarie.
```

## Utilizzo
```
pingapersempre.bat -> Quando è in esecuzione salva l'esito dei ping in un file CSV.
statistiche.bat    -> Produce un file HTML di statistiche sui dati contenuti nel file CSV.
                      Eseguire a piacimento.
```

## Struttura del programma

```
pingapersempre/
│-- config.py          # Unico file di configurazione dove inserire i propri parametri
│-- pingapersempre.csv # file CSV con l'archivio dell'esito dei ping (creato alla prima esecuzione)
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

