# Esempio di Utilizzo - VIM QUIZ GUI v4.1

## 🚀 Avvio Rapido

```bash
# Metodo 1: Script automatico (raccomandato)
./vimquiz.sh

# Metodo 2: Avvio diretto
python3 vimquiz.py
```

## 🆕 Nuove Funzionalità v4.1

- **Internazionalizzazione**: Supporto per 5 lingue europee
- **Rilevamento automatico**: Rileva la lingua di sistema
- **Selettore lingua**: Cambia lingua in tempo reale
- **Traduzioni complete**: Interfaccia e domande tradotte
- **Sistema modulare**: Domande organizzate in file JSON separati
- **Filtri avanzati**: Filtra per categoria e difficoltà
- **Controllo domande**: Imposta il numero di domande (5-100)
- **Statistiche complete**: Visualizza statistiche dettagliate
- **271+ comandi**: Database ampliato con 10 categorie

## 🎮 Interfaccia Utente

### Pannello Superiore
- **Domanda X/Y**: Mostra il progresso del quiz
- **Punteggio**: Punteggio attuale
- **Barra di progresso**: Percentuale completata
- **Lingua**: Selettore per cambiare la lingua dell'interfaccia
- **Filtri**: Categoria, difficoltà e numero di domande
- **Aggiorna Quiz**: Pulsante per applicare i filtri

### Pannello Centrale
- **Descrizione**: Descrizione del comando Vim con categoria e difficoltà
- **Opzioni**: 4 opzioni di risposta (radio buttons)
- **Controlli**: Pulsanti per rispondere e navigare

### Pannello Laterale
- **Risultati**: Feedback in tempo reale
- **Storico**: Risposte corrette e sbagliate con dettagli

## 🎯 Flusso di Utilizzo

1. **Avvia il quiz**: L'applicazione carica automaticamente la prima domanda
2. **Leggi la descrizione**: Comprendi cosa fa il comando Vim
3. **Seleziona la risposta**: Clicca su una delle 4 opzioni
4. **Conferma**: Clicca "Rispondi" per confermare
5. **Vedi il feedback**: L'applicazione mostra se la risposta è corretta
6. **Continua**: Clicca "Prossima Domanda" per procedere
7. **Risultati finali**: Al termine vedi statistiche complete

## 🔧 Funzionalità Avanzate

### Internazionalizzazione
- **Lingue Supportate**: Inglese, Italiano, Spagnolo, Francese, Tedesco
- **Rilevamento Automatico**: Rileva la lingua di sistema all'avvio
- **Cambio Lingua**: Selettore per cambiare lingua in tempo reale
- **Traduzioni Complete**: Interfaccia, menu, messaggi e domande tradotti
- **Fallback**: Sistema di fallback per traduzioni mancanti

### Filtri e Controlli
- **Categoria**: Seleziona una categoria specifica o "Tutte"
- **Difficoltà**: Filtra per livello di difficoltà
- **Numero Domande**: Imposta da 5 a 100 domande
- **Aggiorna Quiz**: Applica i filtri selezionati

### Mescolare Domande
- Clicca "Mescola Domande" per cambiare l'ordine
- Utile per ripetere il quiz con ordine diverso

### Riavviare il Quiz
- Clicca "Riavvia Quiz" per ricominciare
- Il punteggio viene resettato

### Menu
- **Quiz → Nuovo Quiz**: Riavvia il quiz
- **Quiz → Mescola Domande**: Mescola le domande
- **Quiz → Aggiorna Impostazioni**: Applica i filtri
- **Quiz → Statistiche Domande**: Mostra statistiche complete
- **Quiz → Esci**: Chiude l'applicazione
- **Aiuto → Informazioni**: Mostra info sull'app

## 📊 Esempi di Domande

### Esempio 1: Comando di Movimento
**Descrizione**: "move cursor left"
**Opzioni**:
- h
- j
- k
- l

**Risposta corretta**: h

### Esempio 2: Comando di Salvataggio
**Descrizione**: "write (save) and quit"
**Opzioni**:
- :w
- :wq
- :q
- :x

**Risposta corretta**: :wq

### Esempio 3: Comando di Copia
**Descrizione**: "yank (copy) a line"
**Opzioni**:
- yy
- dd
- pp
- cc

**Risposta corretta**: yy

## 🎨 Personalizzazione

### Cambiare il Tema
L'applicazione usa il tema "Fusion" di Qt6. Per cambiarlo, modifica la riga:
```python
app.setStyle('Fusion')
```

### Aggiungere Comandi
Modifica il dizionario `vim_commands` in `vimquiz.py`:
```python
self.vim_commands = {
    "nuovo_comando": "descrizione del comando",
    # ... altri comandi
}
```

## 🐛 Risoluzione Problemi

### L'applicazione non si avvia
```bash
# Verifica Python
python3 --version

# Verifica PyQt6
python3 -c "import PyQt6; print('OK')"

# Installa PyQt6 se necessario
pip3 install PyQt6
```

### Interfaccia non si carica
- Verifica che il display X11/Wayland sia attivo
- Su sistemi headless, usa Xvfb per test virtuali

### Errori di permessi
```bash
chmod +x vimquiz.sh vimquiz.py
```

## 📈 Suggerimenti per l'Uso

1. **Inizia con pochi comandi**: Familiarizza con i comandi base
2. **Usa il feedback**: Leggi sempre le spiegazioni degli errori
3. **Ripeti il quiz**: Mescola le domande per variare l'esperienza
4. **Studia gli errori**: Il pannello risultati mostra cosa hai sbagliato
5. **Pratica regolarmente**: Il quiz è più efficace con sessioni frequenti

## 🎯 Obiettivi di Apprendimento

- **Principiante**: 50-70% di risposte corrette
- **Intermedio**: 70-85% di risposte corrette  
- **Avanzato**: 85-95% di risposte corrette
- **Esperto**: 95-100% di risposte corrette

Buon apprendimento! 🚀
