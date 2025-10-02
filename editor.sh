#!/usr/bin/env bash
# VIM QUIZ - Question Editor Script
# Script di avvio per l'editor delle domande
# ------------------------------------------------------

# Colori per l'output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

echo -e "${BOLD}${BLUE}VIM QUIZ - Question Editor${NC}"
echo -e "${YELLOW}Editor per la modifica delle domande con supporto i18n${NC}"
echo

# Controlla se Python 3 è installato
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Errore: Python 3 non è installato.${NC}"
    echo "Installa Python 3 per continuare."
    exit 1
fi

# Controlla se PyQt6 è installato
if ! python3 -c "import PyQt6" 2>/dev/null; then
    echo -e "${YELLOW}PyQt6 non è installato.${NC}"
    
    # Controlla se esiste già un venv
    if [ -d "venv" ]; then
        echo -e "${BLUE}Trovato ambiente virtuale esistente. Attivazione...${NC}"
        source venv/bin/activate
        
        # Verifica se PyQt6 è installato nel venv
        if ! python -c "import PyQt6" 2>/dev/null; then
            echo -e "${YELLOW}Installazione di PyQt6 nell'ambiente virtuale...${NC}"
            pip install PyQt6
        fi
    else
        echo -e "${BLUE}Creazione di un ambiente virtuale...${NC}"
        
        # Crea il venv
        python3 -m venv venv
        if [ $? -ne 0 ]; then
            echo -e "${RED}Errore: Impossibile creare l'ambiente virtuale.${NC}"
            echo "Installa python3-venv:"
            echo "  sudo apt install python3-venv  # Ubuntu/Debian"
            exit 1
        fi
        
        # Attiva il venv
        source venv/bin/activate
        
        # Installa PyQt6 nel venv
        echo -e "${YELLOW}Installazione di PyQt6 nell'ambiente virtuale...${NC}"
        pip install PyQt6
        
        if [ $? -ne 0 ]; then
            echo -e "${RED}Errore: Impossibile installare PyQt6.${NC}"
            echo "Prova a installare manualmente:"
            echo "  source venv/bin/activate"
            echo "  pip install PyQt6"
            exit 1
        fi
    fi
    
    # Verifica finale
    if ! python -c "import PyQt6" 2>/dev/null; then
        echo -e "${RED}Errore: PyQt6 non è disponibile nell'ambiente virtuale.${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}PyQt6 installato correttamente nell'ambiente virtuale.${NC}"
else
    echo -e "${GREEN}PyQt6 trovato nel sistema.${NC}"
fi

# Controlla se i file necessari esistono
if [ ! -f "question_editor.py" ]; then
    echo -e "${RED}Errore: question_editor.py non trovato.${NC}"
    echo "Assicurati di essere nella directory corretta."
    exit 1
fi

if [ ! -d "questions" ]; then
    echo -e "${RED}Errore: Directory 'questions' non trovata.${NC}"
    echo "Assicurati di essere nella directory corretta."
    exit 1
fi

if [ ! -d "locales" ]; then
    echo -e "${RED}Errore: Directory 'locales' non trovata.${NC}"
    echo "Assicurati di essere nella directory corretta."
    exit 1
fi

echo -e "${GREEN}Avvio dell'editor delle domande...${NC}"
echo

# Avvia l'editor
# Se siamo in un venv, usa 'python', altrimenti 'python3'
if [ -n "$VIRTUAL_ENV" ]; then
    python question_editor.py
else
    python3 question_editor.py
fi

echo -e "${GREEN}Editor chiuso. Grazie per aver usato VIM QUIZ Editor!${NC}"
