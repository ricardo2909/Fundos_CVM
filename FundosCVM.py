import streamlit as st
import pandas as pd
import numpy as np
import requests
import zipfile
import datetime as dt
from datetime import datetime
import os
import pickle
import time
import io
import base64
import hashlib
from io import BytesIO

def submit():
    st.session_state.something = st.session_state.widget
    st.session_state.widget = ''


def dowload_file(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(
        csv.encode()
    ).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}">Download csv file</a>'
    return href


# Definindo a função para consultar os fundos
@st.cache_data()
def consultar_fundos(lista,data,tipo):
    
    ano = data[:4]
    mes = data[4:6]
    url = f"https://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_{ano}{mes}.zip"

    download = requests.get(url)

    with open(f"inf_diario_fi_{ano}{mes}.zip", "wb") as arquivo_cvm:
        arquivo_cvm.write(download.content)

    arquivo_zip = zipfile.ZipFile(f"inf_diario_fi_{ano}{mes}.zip")

    dados_fundos = pd.read_csv(arquivo_zip.open(arquivo_zip.namelist()[0]), sep=";", encoding="ISO-8859-1", dtype= str)

    dados_cadastro = pd.read_csv('https://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv', sep=";", encoding="ISO-8859-1", dtype={'CNPJ_FUNDO': str})

    dados_cadastro = dados_cadastro[['CNPJ_FUNDO', 'DENOM_SOCIAL']]
    dados_cadastro = dados_cadastro.drop_duplicates()

    base_final = pd.merge(dados_fundos, dados_cadastro, how='left', left_on='CNPJ_FUNDO', right_on='CNPJ_FUNDO')

    base_final = base_final[['DT_COMPTC', 'CNPJ_FUNDO', 'DENOM_SOCIAL', 'VL_QUOTA', 'VL_PATRIM_LIQ']]

    dia = int(data[6:8])

    if tipo == 'CNPJ':
        base_filtro = base_final[base_final['CNPJ_FUNDO'].isin(lista)]
    elif tipo == 'NOME':
        base_filtro = base_final[base_final['DENOM_SOCIAL'].isin(lista)]

    base_filtro = base_filtro[base_filtro['DT_COMPTC'] == f"{ano}-{mes}-{dia}"]
    base_filtro = base_filtro[['DT_COMPTC','CNPJ_FUNDO', 'DENOM_SOCIAL', 'VL_QUOTA']]
    base_filtro['VL_QUOTA'] = base_filtro['VL_QUOTA'].str.replace('.', ',')
    return base_filtro

def app():
    
    dados_cadastro = pd.read_csv('https://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv', sep=";", encoding="ISO-8859-1", dtype={'CNPJ_FUNDO': str})

    dados_cadastro = dados_cadastro[['CNPJ_FUNDO', 'DENOM_SOCIAL']]
    dados_cadastro = dados_cadastro.drop_duplicates()

    cnpjs_existentes = dados_cadastro['CNPJ_FUNDO'].tolist()
    nomes_existentes = dados_cadastro['DENOM_SOCIAL'].tolist()

    #colocar tela cheia
    
    # Lendo a lista de CNPJs salvos do arquivo texto
    if os.path.isfile("cnpjs.txt"):
        with open("cnpjs.txt", "r") as arquivo:
            cnpjs_salvos = arquivo.read().splitlines()
    else:
        cnpjs_salvos = []
    
    if os.path.isfile("nomes.txt"):
        with open("nomes.txt", "r") as arquivo:
            nomes_salvos = arquivo.read().splitlines()
    else:
        nomes_salvos = []

    st.title("Consulta de Fundos")


    # Criando as duas caixas de entrada com a classe "input"
    col1, col2 = st.columns(2)
    # Criando as caixas de texto para receber os CNPJs e nomes dos fundos
    with col1:
        cnpj_input = st.multiselect("**Selecione o CNPJ do fundo:**", cnpjs_existentes, key="cnpj_input")
    with col2:
        nome_input = st.multiselect("**Selecione o nome do fundo:**", nomes_existentes)

    

    # Botão para adicionar o CNPJ digitado à lista de CNPJs salvos
    with col1:
        if st.button("Adicionar CNPJ"):
            if cnpj_input:
                for cnpj in cnpj_input:
                    if cnpj not in cnpjs_salvos:
                        # Verificar CNPJ e adicionar à lista
                        cnpjs_salvos.append(cnpj)
                        msg = st.empty()  # criar espaço vazio na interface do usuário
                        msg.success(f"CNPJ {cnpj} adicionado com sucesso!")
                        time.sleep(0.4)  # aguardar 1 segundos
                        msg.empty()  # limpar mensagem após 4 segundoscd ..



                    else:
                        msg = st.empty()
                        msg.warning(f"CNPJ {cnpj} inválido ou já existe na lista.")
                        time.sleep(0.4)
                        msg.empty()
                # Salvando a lista de CNPJs no arquivo texto
                with open("cnpjs.txt", "w") as arquivo:
                    arquivo.write("\n".join(cnpjs_salvos))
            else:
                msg = st.empty()
                msg.warning("Digite um CNPJ.")
                time.sleep(0.4)
                msg.empty()

    with col2:
        if st.button("Adicionar Nome"):
            if nome_input:
                for nome in nome_input:
                    if nome not in nomes_salvos:
                        nomes_salvos.append(nome)
                        msg = st.empty()
                        msg.success(f"Nome {nome} adicionado com sucesso!")
                        time.sleep(0.4)
                        msg.empty()
                    else:
                        msg = st.empty()
                        msg.warning(f"Nome {nome} inválido ou já existe na lista.")
                        time.sleep(0.4)
                        msg.empty()

                with open("nomes.txt", "w") as arquivo:
                    arquivo.write("\n".join(nomes_salvos))
            else:
                msg = st.empty()
                msg.warning("Digite um nome.")
                time.sleep(0.4)
                msg.empty()
    
    # Caixa de seleção para remover um CNPJ da lista
    with col1:
        st.write("\n")
        cnpj_remover = st.multiselect("**Remover CNPJ:**", cnpjs_salvos)

    with col2:
        st.write("\n")
        nome_remover = st.multiselect("**Remover Nome:**", nomes_salvos)

    # Botão para remover o CNPJ selecionado da lista
    with col1:
        if st.button("Remover CNPJ"):
            if cnpj_remover:
                for cnpj in cnpj_remover:
                    cnpjs_salvos.remove(cnpj)
                    msg = st.empty()
                    msg.success("CNPJ removido com sucesso!")
                    time.sleep(0.4)
                    msg.empty()

                # Salvando a lista de CNPJs no arquivo texto
                with open("cnpjs.txt", "w") as arquivo:
                    arquivo.write("\n".join(cnpjs_salvos))
            else:
                msg = st.empty()
                msg.warning("Selecione um CNPJ para remover.")
                time.sleep(0.4)
                msg.empty()

        if st.button("Limpar Lista de CNPJs"):
            if cnpjs_salvos:
                cnpjs_salvos = []
                with open("cnpjs.txt", "w") as arquivo:
                    arquivo.write("")
            else:
                msg = st.empty()
                msg.warning("A lista de CNPJs já está vazia.")
                time.sleep(0.4)
                msg.empty()
            

    with col2:
        if st.button("Remover Nome"):
            if nome_remover:
                for nome in nome_remover:
                    nomes_salvos.remove(nome)
                    msg = st.empty()
                    msg.success("Nome removido com sucesso!")
                    time.sleep(0.4)
                    msg.empty()

                with open("nomes.txt", "w") as arquivo:
                    arquivo.write("\n".join(nomes_salvos))
            else:
                msg = st.empty()
                msg.warning("Selecione um nome para remover.")
                time.sleep(0.4)
                msg.empty()
        
        if st.button("Limpar Lista de Nomes"):
            if nomes_salvos:
                nomes_salvos = []
                with open("nomes.txt", "w") as arquivo:
                    arquivo.write("")
            else:
                msg = st.empty()
                msg.warning("A lista de nomes já está vazia.")
                time.sleep(0.4)
                msg.empty()

    st.write("\n")
    # Botão para exibir/ocultar a tabela com a lista de CNPJs salvos
    with col1:
        st.write("\n")
        exibir_tabela = st.checkbox("**Mostrar lista de CNPJs salvos**")

    with col2:
        st.write("\n")
        exibir_tabela2 = st.checkbox("**Mostrar lista de nomes salvos**")

    if exibir_tabela:
        with open("cnpjs.txt", "r") as arquivo:
            cnpjs_salvos = arquivo.read().splitlines()
        if cnpjs_salvos:
            with col1:
                st.write("CNPJs salvos:")
                for cnpj in cnpjs_salvos:
                    st.write(f"- {cnpj}")
                st.write("\n")
        else:
            st.warning("Não há CNPJs salvos.")
    
    if exibir_tabela2:
        with open("nomes.txt", "r") as arquivo:
            nomes_salvos = arquivo.read().splitlines()
        if nomes_salvos:
            with col2:
                st.write("Nomes salvos:")
                for nome in nomes_salvos:
                    st.write(f"- {nome}")
                st.write("\n")
        else:
            st.warning("Não há nomes salvos.")

    st.write("**Consultar por:**")

    tipo = st.radio("**Consultar por:**", ["CNPJ", "NOME"],horizontal=True)


    # if cnpjs_salvos and not nomes_salvos:
    #     tipo = st.selectbox("**Consultar por:**", ["CNPJ"])
    # elif nomes_salvos and not cnpjs_salvos:
    #     tipo = st.selectbox("**Consultar por:**", ["NOME"])
    # elif cnpjs_salvos and nomes_salvos:
    #     tipo = st.selectbox("**Consultar por:**", ["CNPJ", "NOME"])
    # else:
    #     st.warning("Não há CNPJs ou nomes salvos.")
    #pegar a data de hoje - 2 e transformar no padrao aceito pela API
    data_padrao =  dt.date.today() - dt.timedelta(days=2)

    data = st.date_input("Selecione a data que deseja consultar", value=data_padrao, max_value=dt.date.today())
    # Se houver CNPJs salvos, exibe o campo para selecionar a data e o botão para consulta
    #criar botao

    click = st.button("Consultar")
    if tipo and click and data:
        
        if tipo == "CNPJ":
            lista = cnpjs_salvos
        else:
            lista = nomes_salvos
        # Formatando a data para o formato AAAAMMDD
        data_str = data.strftime('%Y%m%d')

        # Chamando a função para consultar os fundos
        resultado = consultar_fundos(lista, data_str, tipo)

        # Exibindo o resultado na tela
        if resultado.empty:
            st.warning("Não foram encontrados resultados para os CNPJs e a data informados.")
        else:
            st.write(resultado)
            nome_arquivo = st.text_input("Digite o nome do arquivo para salvar (sem extensão)", value = f"Fundos_{data_str}", max_chars=50)
            # Botão para exportar a tabela resultante em diferentes formatos

            if st.button("Exportar tabela"):
                csv = dowload_file(resultado)
            st.download_button("Exportar tabela", csv, file_name=f"{nome_arquivo}.xlsx")
    elif tipo and click and not data:
        st.warning("Selecione uma data para consultar.")
    elif data and click and not tipo:
        st.warning("Selecione o tipo de consulta.")
    elif click and not data and not tipo:
        st.warning("Selecione o tipo de consulta e a data.")
    elif tipo and data and not click:
        st.warning("Clique no botão 'Consultar' para iniciar a consulta.")


if __name__ == "__main__":
    app()
