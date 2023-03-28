import streamlit as st
import FundosCVM  # importa o seu script FundosCVM.py

# Define a página inicial
def homepage():
    st.title("Consulta de Fundos CVM")
    st.write("Insira os CNPJs dos fundos que deseja consultar e selecione a data:")

    # Campo de entrada para CNPJ
    cnpj_input = st.text_input("Insira o CNPJ do fundo:")

    # Campo de seleção de data
    data_input = st.date_input("Selecione a data da consulta:")

    # Botão para executar a consulta
    if st.button("Consultar"):
        resultado = FundosCVM.consultar_fundos([cnpj_input], data_input) # Chama a função do seu script FundosCVM.py
        st.write(resultado)

# Inicializa o app
def main():
    st.set_page_config(page_title="Consulta de Fundos CVM")
    homepage()

if __name__ == "__main__":
    main()
