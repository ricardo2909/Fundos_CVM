#!/bin/bash
set -e

# Instala o pacote heroku-cli no ambiente Heroku
npm install -g heroku

# Define um diretório para os arquivos de configuração do Streamlit
mkdir -p ~/.streamlit

# Cria o arquivo de configuração do Streamlit
cat > ~/.streamlit/config.toml <<- EOM
[server]
headless = true
port = $PORT
enableCORS = false
EOM