#!/bin/bash

# Ścieżki do komponentów aplikacji
APP_PATH="$HOME/Pulpit/FortiPass/src/main.py"
VENV_PATH="$HOME/Pulpit/FortiPass/venv/bin/activate"

# Włącz środowisko wirtualne i uruchom aplikację
source "$VENV_PATH"
python3 "$APP_PATH"
