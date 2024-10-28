[English](README.md) | [Italiano](README.it.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Español](README.es.md)

# Lisa - Analizzatore di Codice per LLM

Lisa (ispirato a Lisa Simpson) è uno strumento progettato per semplificare l'analisi del codice sorgente attraverso i Large Language Models (LLM). Intelligente e analitica come il personaggio da cui prende il nome, Lisa aiuta a studiare e interpretare il codice con logica e metodo.

## Descrizione

Lisa è uno strumento essenziale per chi vuole analizzare il proprio codice o studiare progetti open source attraverso i Large Language Models. Il suo principale obiettivo è generare un unico file di testo che mantiene tutti i riferimenti e la struttura del codice originale, rendendolo facilmente interpretabile da un LLM.

Questo approccio risolve uno dei problemi più comuni nell'analisi del codice con gli LLM: la frammentazione dei file e la perdita dei riferimenti tra i diversi componenti del progetto.

## Installazione

Lisa è disponibile come pacchetto Python su PyPI. Per installarlo, esegui:

```bash
pip install hyperlisa
```

L'installazione, in automatico, senza che sia necessario un tuo intervento:
- Crea una cartella `hyperlisa` nel progetto corrente
- Copia all'interno della cartella un file `config.yaml` personalizzabile
- Rende disponibili diversi comandi da terminale per l'esecuzione
- Se presente un file `.gitignore`, aggiunge la cartella `hyperlisa` alle esclusioni

### Comandi disponibili
Dopo l'installazione, puoi utilizzare uno dei seguenti comandi:
```bash
cmb [opzioni]               # Comando breve
lisacmb [opzioni]          # Comando descrittivo
hyperlisacmb [opzioni]     # Comando completo
combine-code [opzioni]      # Comando originale
```

> **Nota**: La disponibilità di più comandi garantisce che almeno uno sia sempre utilizzabile, anche in presenza di potenziali conflitti con altri alias definiti nel sistema.

## Configurazione

Il pacchetto crea un file `config.yaml` nella cartella `hyperlisa` che permette di personalizzare quali file includere o escludere dall'analisi. La configurazione predefinita è:

```yaml
# Pattern di inclusione (estensioni o directory da includere)
includes:
  - "*.py"  
  # È possibile aggiungere altre estensioni o directory

# Pattern di esclusione (directory o file da escludere)
excludes:
  - ".git"
  - "__pycache__"
  - "*.egg-info"
  - "venv*"
  - ".vscode"
  - "agents*"
  - "log"
```

### Pattern di Inclusione/Esclusione
- I pattern in `includes` determinano quali file verranno processati (es: "*.py" include tutti i file Python)
- I pattern in `excludes` specificano quali file o directory ignorare
- È possibile utilizzare il carattere * come carattere jolly
- I pattern vengono applicati sia ai nomi dei file che ai percorsi delle directory
- **Importante**: Le regole di esclusione hanno sempre la priorità su quelle di inclusione

### Priorità delle Regole
Quando ci sono "conflitti" tra regole di inclusione e di esclusione, quelle di esclusione hanno sempre la precedenza. Ecco alcuni esempi:

```
Esempio 1:
/goofy
    /src_code
        /utils
            /logs
                file1.py
                file2.py
            helpers.py
```
Se nelle regole abbiamo:
- includes: ["*.py"]
- excludes: ["*logs"]

In questo caso, `file1.py` e `file2.py` NON verranno inclusi nonostante abbiano l'estensione .py, perché si trovano in una directory che soddisfa il pattern di esclusione "*logs". Il file `helpers.py` invece verrà incluso.

```
Esempio 2:
/goofy
    /includes_dir
        /excluded_subdir
            important.py
```
Se nelle regole abbiamo:
- includes: ["includes_dir"]
- excludes: ["*excluded*"]

In questo caso, `important.py` NON verrà incluso perché si trova in una directory che soddisfa un pattern di esclusione, anche se la sua directory padre soddisfa un pattern di inclusione.

## Utilizzo

Dopo l'installazione, puoi eseguire Lisa usando uno dei comandi disponibili:

```bash
cmb [opzioni]
```

### Struttura e Nome Predefinito
Per comprendere quale nome file verrà utilizzato di default, consideriamo questa struttura:

```
/home/user/progetti
    /goofy     <- Questa è la directory root
        /hyperlisa
            config.yaml
            GOOFY_20240325_1423.txt
            GOOFY_20240326_0930.txt
        /src
            main.py
        /tests
            test_main.py
```

In questo caso, il nome predefinito sarà "GOOFY" (il nome della directory root in maiuscolo).

### Parametri disponibili:

- `--clean`: Rimuove tutti i file di testo precedentemente generati
- `--output NOME`: Specifica il prefisso del nome del file di output
  ```bash
  # Esempio con nome predefinito (dalla struttura sopra)
  cmb
  # Output: GOOFY_20240327_1423.txt

  # Esempio con nome personalizzato
  cmb --output ANALISI_GOOFY
  # Output: ANALISI_GOOFY_20240327_1423.txt
  ```

#### Esempio di utilizzo di --clean

Supponiamo di avere questa situazione iniziale:
```
/goofy
    /hyperlisa
        config.yaml
        GOOFY_20240325_1423.txt
        GOOFY_20240326_0930.txt
        GOOFY_20240326_1645.txt
```

Dopo l'esecuzione di `cmb --clean`:
```
/goofy
    /hyperlisa
        config.yaml
        GOOFY_20240327_1430.txt    # Nuovo file generato
```

Il comando `--clean` rimuove tutti i file .txt precedenti che iniziano con lo stesso prefisso prima di generare il nuovo file. Questo è utile quando si vuole mantenere solo l'ultima versione dell'analisi.

### Output

Lo script genera un file di testo con il formato:
`NOME_YYYYMMDD_HHMM.txt`

dove:
- `NOME` è il prefisso specificato con --output o quello predefinito
- `YYYYMMDD_HHMM` è il timestamp di generazione

## Utilizzo con Progetti GitHub

Per utilizzare Lisa con un progetto GitHub, segui questi passaggi:

1. **Preparazione dell'ambiente**:
   ```bash
   # Crea e accedi a una directory per i tuoi progetti
   mkdir ~/progetti
   cd ~/progetti
   ```

2. **Clona il progetto da analizzare**:
   ```bash
   # Esempio con un progetto ipotetico "goofy"
   git clone goofy.git
   cd goofy
   ```

3. **Installa Lisa**:
   ```bash
   pip install hyperlisa
   ```

4. **Personalizza la configurazione** (opzionale):
   ```bash
   # Il file config.yaml si trova nella cartella hyperlisa
   # Modifica le regole di inclusione/esclusione secondo necessità
   ```

5. **Esegui l'analisi**:
   ```bash
   cmb
   ```

> **Nota**: Durante l'installazione, Lisa controlla automaticamente la presenza del file .gitignore e, se presente, aggiunge la cartella 'hyperlisa' alle esclusioni. Questo assicura che i file generati non vengano accidentalmente inclusi nel repository.

### Migliori Pratiche per l'Analisi
- Prima di eseguire Lisa, assicurati di essere nella directory root del progetto da analizzare
- Controlla e personalizza il file `config.yaml` in base alle specifiche necessità del progetto
- Utilizza l'opzione `--clean` per mantenere ordinata la directory quando generi multiple versioni

## Note Aggiuntive

- Lisa mantiene la struttura gerarchica dei file nel documento generato
- Ogni file viene chiaramente delimitato da separatori che ne indicano il percorso relativo
- Il codice viene organizzato mantenendo l'ordine di profondità delle directory
- I file generati vengono salvati nella cartella `hyperlisa` e possono essere facilmente condivisi con gli LLM per l'analisi

## Contribuire

Se vuoi contribuire al progetto, puoi:
- Aprire segnalazioni per riportare bug o proporre miglioramenti
- Proporre richieste di integrazione con nuove funzionalità
- Migliorare la documentazione
- Condividere i tuoi casi d'uso e suggerimenti

## Licenza

Licenza MIT

Copyright (c) 2024

È concesso gratuitamente il permesso a chiunque ottenga una copia
di questo software e dei relativi file di documentazione (il "Software"), di trattare
il Software senza restrizioni, inclusi, senza limitazioni, i diritti
di utilizzare, copiare, modificare, unire, pubblicare, distribuire, concedere in sublicenza e/o vendere
copie del Software, e di permettere alle persone a cui il Software è
fornito di farlo, alle seguenti condizioni:

L'avviso di copyright sopra riportato e questo avviso di permesso devono essere inclusi in
tutte le copie o parti sostanziali del Software.

IL SOFTWARE VIENE FORNITO "COSÌ COM'È", SENZA GARANZIE DI ALCUN TIPO, ESPLICITE O
IMPLICITE, INCLUSE, MA NON SOLO, LE GARANZIE DI COMMERCIABILITÀ,
IDONEITÀ PER UN PARTICOLARE SCOPO E NON VIOLAZIONE. IN NESSUN CASO GLI
AUTORI O I TITOLARI DEL COPYRIGHT SARANNO RESPONSABILI PER QUALSIASI RECLAMO, DANNO O ALTRA
RESPONSABILITÀ, SIA IN UN'AZIONE DI CONTRATTO, ILLECITO O ALTRO, DERIVANTE DA,
FUORI O IN CONNESSIONE CON IL SOFTWARE O L'USO O ALTRE OPERAZIONI NEL
SOFTWARE.