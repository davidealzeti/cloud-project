# Analisi della distribuzione dei vaccini

L'analisi della distribuzione dei vaccini è stata fatta prendendo come riferimento gli open data disponibili a questo link: [File Analisi](https://github.com/italia/covid19-opendata-vaccini/blob/master/dati/consegne-vaccini-latest.csv)

## Features

- Lettura di un file .csv contenente i dati sulla distribuzione dei vaccini in Italia
- Scelta del tipo di analisi da effettuare
- Salvataggio delle analisi effettuate
- Distribuzione delle funzionalità tramite **Docker**

## Tech

Principali pacchetti *Python* utilizzati durante lo sviluppo:

- pandas==1.2.4
- numpy==1.20.3
- requests~=2.25.1

Gli altri necessari per la build sono inclusi nel file *requirements.txt*

## Installation

Per l'installazione va scaricato l'intero progetto. Successivamente va fatta la build del *dockerfile* all'ìnterno della directory in cui è contenuto il file:

```sh
docker build ./
```

Una volta avvenuta la build del *dockerfile* sarà possibile accedere alle funzionalità del programma.


## Docker

Il docker può essere lanciato impostando alcune variabili d'ambiente per ottenere diverse funzionalità.

### Tipo di analisi

La variabile **SELECTED_ANALYSIS** assume un valore tra *0* e *3* per selezionare il tipo di analisi.

- **0** per avere il numero di vaccini totali per area (regione)
- **1** per avere il numero di dosi consegnate per ciascun fornitore
- **2** per avere il numero di vaccini totali consegnati per ciascun mese
- **3** per avere la percentuale di vaccini consegnati per area rispetto al totale

### Salvataggio del file

La variabile **SAVE_FILE** assume un valore booleano *True* o *False* per specificare se salvare o meno i risultati delle analisi in un file.
> **Attenzione**: se si vuole ottenere la permanenza del file anche dopo la chiusura del docker occorre collegare un volume e associarlo alla cartella **/saved_files**

### Formato del file

La variabile **FILE_FORMAT** specifica il formato dell'output delle analisi e, se specificato, il formato del file in cui le analisi vengono salvate; può assumere 3 valori:

- **txt** per il formato testuale
- **csv** per il formato *comma separated values*
- **json** per il formato JSON

> Se non specificato, il valore di default è JSON

### Lettura del file da Github

La variabile **GET_FILE_FROM_GITHUB** assume un valore booleano *True* o *False* per specificare se leggere o meno i dati dal file di riferimento presente su Github, in modo tale da poter avere i dati aggiornati ai valori più recenti.

> Di default il programma leggerà dei valori da un file salvato in memoria

## Codice Interessante & Twelve Factors

### Dependencies

Le dipendenze sono state dichiarate esplicitamente e sono state isolate nel file *requirements.txt*

### Dev/prod parity

Le fasi di development, staging e production sono state mantenute il più possibile simili tra loro

### Backing services

I servizi sono stati trattati come risorse statiche


![Immagine](https://github.com/davidealzeti/cloud-project/blob/main/code.png)
