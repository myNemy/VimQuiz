#!/usr/bin/env bash
# VIM QUIZ - Script di avvio per la versione GUI Qt6
# ------------------------------------------------------

# Colori per l'output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

echo -e "${BOLD}${BLUE}VIM QUIZ - Quiz interattivo per imparare i comandi Vim${NC}"
echo -e "${YELLOW}Versione GUI Qt6${NC}"
echo

# Controlla se Python 3 è installato
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Errore: Python 3 non è installato.${NC}"
    echo "Installa Python 3 per continuare."
    exit 1
fi

# Controlla se PyQt6 è installato
if ! python3 -c "import PyQt6" 2>/dev/null; then
    echo -e "${YELLOW}PyQt6 non è installato. Installazione in corso...${NC}"
    
    # Prova a installare PyQt6
    if command -v pip3 &> /dev/null; then
        pip3 install PyQt6
    elif command -v pip &> /dev/null; then
        pip install PyQt6
    else
        echo -e "${RED}Errore: pip non è installato.${NC}"
        echo "Installa pip e PyQt6 per continuare:"
        echo "  sudo apt install python3-pip  # Ubuntu/Debian"
        echo "  pip3 install PyQt6"
        exit 1
    fi
    
    # Verifica se l'installazione è riuscita
    if ! python3 -c "import PyQt6" 2>/dev/null; then
        echo -e "${RED}Errore: Impossibile installare PyQt6.${NC}"
        echo "Installa manualmente PyQt6:"
        echo "  pip3 install PyQt6"
        exit 1
    fi
fi

echo -e "${GREEN}Avvio del VIM QUIZ...${NC}"
echo

# Avvia l'applicazione Python
python3 vimquiz.py

echo -e "${GREEN}Grazie per aver usato VIM QUIZ!${NC}"