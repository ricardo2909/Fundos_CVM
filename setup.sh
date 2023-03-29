#!/bin/bash
set -e

# Define um diretório para os arquivos de configuração do Streamlit
mkdir -p ~/.streamlit

# Cria o arquivo de configuração do Streamlit
cat > ~/.streamlit/config.toml <<- EOM
[server]
headless = true
port = $PORT
enableCORS = false
EOM