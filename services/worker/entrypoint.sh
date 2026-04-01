#!/bin/bash
set -e

# Caminho para um arquivo oculto que indica que a instalação foi concluída
INSTALL_FLAG="/home/appuser/.cache/pip/.dissmodel_installed"

echo "🔧 DisSModel Worker Starting..."

if [ -d "/opt/dissmodel" ]; then
    # Só instala se o arquivo 'flag' não existir
    if [ ! -f "$INSTALL_FLAG" ]; then
        echo "📦 Installing dissmodel and ALL dependencies (this may take a while)..."
        
        # O pip install -e vai ler o setup.py/pyproject.toml e baixar tudo
        pip install -e /opt/dissmodel
        
        # Cria o flag para que no próximo boot ele pule esta etapa
        touch "$INSTALL_FLAG"
        echo "✅ dissmodel and dependencies installed successfully."
    else
        echo "✅ Dependencies already cached. Skipping installation."
    fi
else
    echo "ℹ️  No development volume found at /opt/dissmodel."
fi

echo "🚀 Starting worker..."
exec python -m worker.worker "$@"