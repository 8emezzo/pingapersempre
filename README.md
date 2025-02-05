# pingapersempre

## Descrizione
Monitora nel tempo i ping verso un elenco di IP
```
Salva l'esito dei ping in un file CSV e ciclicamente produce delle statistiche in un file HTML
```

## Requisiti
Assicurati di avere installato Python nella macchina
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
Editare il file config.py ed inserire gli IP da monitorare.
Eventualmente mofificare i parametri della configurazione di default.
```

## Utilizzo
```
pingapersempre.bat
```
Schermata di runtime:
![Schermata di runtime](images/runtime.png)

Output statistiche:
![statistiche_1.png](images/statistiche_1.png)
![statistiche_2.png](images/statistiche_2.png)
![statistiche_3.png](images/statistiche_3.png)



## Struttura del programma

```
pingapersempre/
│-- config.py          # file di configurazione
│-- main.py            # file py principale
│-- statistiche.py     # file py statistiche
│-- requirements.txt   # elenco librerie Python
│-- pingapersempre.csv # file CSV con l'archivio dell'esito dei ping (creato alla prima esecuzione)
│-- pingapersempre.bat # lancia il programma
│-- install.bat        # installa le librerie Python contenute in requirements.txt
│-- statistiche.bat    # forza l'aggiornamento del file HTML delle statistiche
│-- statistiche.html   # file HTML con le statistiche (creato alla prima esecuzione)
│-- README.md          # questo file
```

## Contatti
```
Per domande o suggerimenti, ma soprattutto schei, contattami a simoneventurin [chiocciola] gmail.com
```

## Licenza
```
Questo progetto è distribuito sotto la licenza MIAO LOL
(Modello Indipendente Antani Open - Licenza Operativa Libera)
```

