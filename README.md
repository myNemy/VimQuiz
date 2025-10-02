# VIM QUIZ - Quiz Interattivo per Imparare i Comandi Vim

Un'applicazione GUI moderna per imparare i comandi Vim attraverso un quiz interattivo con sistema modulare delle domande.

## 🚀 Caratteristiche

- **Interfaccia grafica moderna** con Qt6
- **271+ comandi Vim** organizzati in 10 categorie
- **Sistema modulare** per le domande (file JSON separati)
- **Internazionalizzazione (i18n)** con supporto per 5 lingue
- **Filtri avanzati** per categoria e difficoltà
- **Quiz interattivo** con opzioni multiple
- **Tracciamento del punteggio** in tempo reale
- **Possibilità di mescolare** le domande
- **Controllo del numero di domande** (5-100)
- **Risultati dettagliati** con errori e spiegazioni
- **Statistiche complete** sulle domande
- **Interfaccia intuitiva** e user-friendly

## 📋 Requisiti

- Python 3.6 o superiore
- PyQt6
- Sistema operativo Linux/Windows/macOS

## 🛠️ Installazione

### Metodo 1: Script automatico (Raccomandato)
```bash
./vimquiz.sh
```
Lo script installerà automaticamente PyQt6 se necessario.

### Metodo 2: Installazione manuale
```bash
# Installa PyQt6
pip3 install PyQt6

# Avvia l'applicazione
python3 vimquiz.py
```

## 🎮 Utilizzo

### Avvio dell'Applicazione
```bash
# Metodo 1: Script automatico (raccomandato)
./vimquiz.sh

# Metodo 2: Avvio diretto
python3 vimquiz.py
```

**Interfaccia principale**:
- **Pannello superiore**: Informazioni sul quiz e progresso
- **Pannello centrale**: Domanda e opzioni di risposta
- **Pannello inferiore**: Controlli del quiz
- **Pannello laterale**: Risultati in tempo reale

**Controlli disponibili**:
- **Rispondi**: Conferma la risposta selezionata
- **Prossima Domanda**: Passa alla domanda successiva
- **Riavvia Quiz**: Ricomincia il quiz
- **Mescola Domande**: Mescola l'ordine delle domande

## 📊 Comandi Vim Inclusi

Il quiz include **271+ comandi Vim** organizzati in **10 categorie**:

### Categorie Disponibili:
- **File Operations** (15 domande): `:w`, `:wq`, `:x`, `:q`, `:q!`, `:qa`, `ZZ`, `ZQ`, `:e`, `:r`, etc.
- **Basic Movement** (28 domande): `h`, `j`, `k`, `l`, `w`, `W`, `e`, `E`, `b`, `B`, `0`, `^`, `$`, `G`, etc.
- **Screen Movement** (14 domande): `Ctrl+u`, `Ctrl+b`, `Ctrl+d`, `Ctrl+f`, `zz`, `zt`, `zb`, etc.
- **Insert Mode** (14 domande): `i`, `I`, `a`, `A`, `o`, `O`, `ea`, `Esc`, `R`, `gI`, etc.
- **Editing** (42 domande): `r`, `J`, `cc`, `cw`, `c$`, `s`, `S`, `xp`, `u`, `Ctrl+r`, `.`, `ciw`, `diw`, etc.
- **Copy/Paste** (43 domande): `yy`, `2yy`, `yw`, `y$`, `p`, `P`, `dd`, `2dd`, `dw`, `D`, `d$`, `x`, etc.
- **Search and Replace** (31 domande): `*`, `/pattern`, `?pattern`, `n`, `N`, `:%s/old/new/g`, etc.
- **Visual Mode** (24 domande): `v`, `V`, `Ctrl+v`, `aw`, `as`, `ap`, `iw`, `is`, `ip`, etc.
- **Marks and Jumps** (25 domande): `ma`, `'a`, `''`, `Ctrl+o`, `Ctrl+i`, etc.
- **Macros** (35 domande): `qa`, `q`, `@a`, `@@`, `:reg`, `"ayy`, `"ap`, etc.

## 🎯 Come Funziona

1. **Selezione domanda**: L'applicazione seleziona casualmente un comando Vim
2. **Generazione opzioni**: Crea 4 opzioni di risposta (1 corretta + 3 distrattori)
3. **Risposta utente**: L'utente seleziona la risposta che ritiene corretta
4. **Valutazione**: L'applicazione valuta la risposta e aggiorna il punteggio
5. **Feedback**: Mostra se la risposta è corretta o sbagliata con spiegazioni
6. **Risultati finali**: Al termine mostra statistiche complete e errori

## 🔧 Personalizzazione

### Aggiungere nuovi comandi
Il sistema modulare permette di aggiungere facilmente nuovi comandi:

1. **Aggiungi a una categoria esistente**: Modifica il file JSON nella cartella `questions/`
2. **Crea una nuova categoria**: Crea un nuovo file JSON seguendo la struttura:

```json
{
  "category": "Nuova Categoria",
  "description": "Descrizione della categoria",
  "difficulty": "beginner|intermediate|advanced",
  "questions": [
    {
      "command": "nuovo_comando",
      "description": "descrizione del comando",
      "category": "sottocategoria"
    }
  ]
}
```

### Struttura dei file delle domande
Ogni file JSON nella cartella `questions/` contiene:
- `category`: Nome della categoria
- `description`: Descrizione della categoria
- `difficulty`: Livello di difficoltà generale
- `questions`: Array di domande con:
  - `command`: Comando Vim
  - `description`: Descrizione del comando
  - `category`: Sottocategoria (opzionale)

### Aggiungere nuove lingue
Il sistema i18n supporta facilmente l'aggiunta di nuove lingue:

1. **Crea una nuova directory** nella cartella `locales/` (es. `locales/pt/` per il portoghese)
2. **Copia i file di traduzione** da una lingua esistente
3. **Traduci i contenuti** nei file `main.json` e `questions.json`
4. **Riavvia l'applicazione** - la nuova lingua apparirà automaticamente nel selettore

### Struttura dei file di traduzione
Ogni lingua ha due file JSON:
- `main.json`: Traduzioni dell'interfaccia principale
- `questions.json`: Traduzioni delle categorie e difficoltà

### Modificare l'interfaccia
L'interfaccia è completamente personalizzabile modificando i metodi `init_ui()` e `create_menu_bar()`.

## 📁 Struttura File

```
VIMQ/
├── vimquiz.py              # Applicazione GUI Python (PyQt6)
├── questions_loader.py     # Sistema di caricamento delle domande
├── i18n_manager.py         # Sistema di internazionalizzazione
├── test_i18n.py           # Test per il sistema i18n
├── vimquiz.sh              # Script di avvio automatico
├── requirements.txt        # Dipendenze Python
├── README.md              # Documentazione principale
├── example_usage.md       # Guida all'utilizzo
├── questions/             # Directory delle domande modulari
│   ├── file_operations.json
│   ├── basic_movement.json
│   ├── screen_movement.json
│   ├── insert_mode.json
│   ├── editing.json
│   ├── copy_paste.json
│   ├── search_replace.json
│   ├── visual_mode.json
│   ├── marks_jumps.json
│   └── macros.json
└── locales/               # Directory delle traduzioni
    ├── en/                # Inglese (lingua base)
    │   ├── main.json
    │   └── questions.json
    ├── it/                # Italiano
    │   ├── main.json
    │   └── questions.json
    ├── es/                # Spagnolo
    │   ├── main.json
    │   └── questions.json
    ├── fr/                # Francese
    │   ├── main.json
    │   └── questions.json
    └── de/                # Tedesco
        ├── main.json
        └── questions.json
```

## 🐛 Risoluzione Problemi

### PyQt6 non si installa
```bash
# Su Ubuntu/Debian
sudo apt update
sudo apt install python3-pip python3-pyqt6

# Su Arch Linux
sudo pacman -S python-pyqt6

# Installazione manuale
pip3 install --user PyQt6
```

### L'applicazione non si avvia
```bash
# Verifica Python
python3 --version

# Verifica PyQt6
python3 -c "import PyQt6; print('PyQt6 installato correttamente')"

# Avvia con debug
python3 -v vimquiz.py
```

## 📝 Changelog

### Versione 4.1 (Internazionalizzazione)
- ✅ Sistema di internazionalizzazione (i18n) completo
- ✅ Supporto per 5 lingue: Inglese, Italiano, Spagnolo, Francese, Tedesco
- ✅ Rilevamento automatico della lingua di sistema
- ✅ Selettore di lingua nell'interfaccia
- ✅ Traduzioni complete per interfaccia e domande
- ✅ Sistema di fallback per traduzioni mancanti
- ✅ Test automatici per il sistema i18n

### Versione 4.0 (Sistema Modulare)
- ✅ Sistema modulare per le domande (file JSON separati)
- ✅ 271+ comandi Vim organizzati in 10 categorie
- ✅ Filtri avanzati per categoria e difficoltà
- ✅ Controllo del numero di domande (5-100)
- ✅ Statistiche complete sulle domande
- ✅ Sistema di caricamento dinamico
- ✅ Interfaccia migliorata con controlli aggiuntivi

### Versione 3.0 (GUI Qt6)
- ✅ Interfaccia grafica moderna con Qt6
- ✅ Quiz interattivo con opzioni multiple
- ✅ Tracciamento punteggio in tempo reale
- ✅ Risultati dettagliati con errori
- ✅ Possibilità di mescolare domande
- ✅ Menu e controlli intuitivi

### Versione 2.x (Terminale)
- Quiz a riga di comando
- Sistema di debug
- Modalità quiet e verbose

## 🤝 Contributi

I contributi sono benvenuti! Per contribuire:

1. Fork del repository
2. Crea un branch per la tua feature
3. Commit delle modifiche
4. Push al branch
5. Crea una Pull Request

## 📄 Licenza

Questo progetto è rilasciato sotto licenza MIT. Vedi il file LICENSE per i dettagli.

## 🙏 Ringraziamenti

- **Vim Community** per la documentazione dei comandi
- **Qt/PyQt** per il framework GUI
- **Python** per la semplicità di sviluppo

---

**Buon apprendimento dei comandi Vim!** 🎉
