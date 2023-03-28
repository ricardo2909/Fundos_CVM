import pandas as pd
import requests
import zipfile
import datetime as dt
import pandas as pd
from openpyxl import load_workbook

hoje = dt.datetime.today().strftime('%Y%m%d')
hoje
ano = hoje[:4]
mes = hoje[4:6]
dia = hoje[6:]
ano, mes, dia

url = f"https://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_{ano}{mes}.zip"

import glob
import os
for f in glob.glob("*.zip"):
    os.remove(f)

download = requests.get(url)

with open(f"inf_diario_fi_{ano}{mes}.zip", "wb") as arquivo_cvm:
    arquivo_cvm.write(download.content)

arquivo_zip = zipfile.ZipFile(f"inf_diario_fi_{ano}{mes}.zip")

dados_fundos = pd.read_csv(arquivo_zip.open(arquivo_zip.namelist()[0]), sep=";", encoding="ISO-8859-1", dtype= str)

dados_cadastro = pd.read_csv('https://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv', sep=";", encoding="ISO-8859-1")

dados_cadastro = dados_cadastro[['CNPJ_FUNDO', 'DENOM_SOCIAL']]
dados_cadastro = dados_cadastro.drop_duplicates()

base_final = pd.merge(dados_fundos, dados_cadastro, how='left', left_on='CNPJ_FUNDO', right_on='CNPJ_FUNDO')

base_final = base_final[['DT_COMPTC', 'CNPJ_FUNDO', 'DENOM_SOCIAL', 'VL_QUOTA', 'VL_PATRIM_LIQ']]

def atualizar_cnpjs(novos_cnpjs):
    global lista_cnpjs
    lista_cnpjs = novos_cnpjs

atualizar_cnpjs(['43.677.242/0001-27',
 '32.302.284/0001-67',
 '20.852.239/0001-05',
 '13.950.115/0001-99'])


dia = int(hoje[6:]) - 10
#filtrar para achar o o VL_QUOTA dos CNPJS no dia de hoje menos 2
base_filtro = base_final[base_final['CNPJ_FUNDO'].isin(lista_cnpjs)] #filtrar para achar o o VL_QUOTA dos CNPJS no dia de hoje menos 2
base_filtro = base_filtro[base_filtro['DT_COMPTC'] == f"{ano}-{mes}-{dia}"] #filtrar para achar o o VL_QUOTA dos CNPJS no dia de hoje menos 2
#Mostrar apenas os campos CNPJ_FUNDO, DENOM_SOCIAL, VL_QUOTA
base_filtro = base_filtro[['DT_COMPTC','CNPJ_FUNDO', 'DENOM_SOCIAL', 'VL_QUOTA']]
#coverter o campo VL_QUOTA para numero sem diminuir a precisão
#converter ponto para virgula na coluna VL_QUOTA
base_filtro['VL_QUOTA'] = base_filtro['VL_QUOTA'].str.replace('.', ',')

#salvar num arquivo excel na aba do dia
# nome_da_aba = f"{dia}_{mes}_{ano}"
# nome_arquivo = "Fundos_CVM.xlsx"
# book = load_workbook(nome_arquivo)
# if nome_da_aba in book.sheetnames:
#     # se a aba já existe, sobrescreve os dados
#     writer = pd.ExcelWriter(nome_arquivo, engine='openpyxl')
#     writer.book = book
#     writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
#     base_filtro.to_excel(writer, sheet_name=nome_da_aba, index=False)
#     writer.save()
# else:
#     # se a aba não existe, cria uma nova aba
#     with pd.ExcelWriter(nome_arquivo, engine='openpyxl') as writer:
#         writer.book = book
#         base_filtro.to_excel(writer, sheet_name=nome_da_aba, index=False)
#         writer.save()