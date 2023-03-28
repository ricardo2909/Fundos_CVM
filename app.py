import streamlit as st
from nbconvert import PythonExporter
import nbformat

# Converter o arquivo .ipynb em um script Python
exporter = PythonExporter()
code, _ = exporter.from_notebook_node(nb)

# Executar o código Python em um novo contexto
with open('FundosCVM.ipynb') as fh:
    nb = nbformat.reads(fh.read(), nbformat.NO_CONVERT)
exec(compile(code, '<string>', 'exec'), globals(), locals())

# Inicializar a lista de CNPJs
cnpjs = []

# Adicionar um botão para inserir um novo CNPJ na lista
cnpj_input = st.text_input("Insira um CNPJ:")
if st.button("Adicionar CNPJ"):
    if cnpj_input:
        cnpjs.append(cnpj_input)

# Adicionar um widget de calendário para selecionar a data da consulta
data_input = st.date_input("Selecione a data da consulta:")

# Adicionar uma lista dos CNPJs inseridos com a opção de excluí-los
st.write("CNPJs inseridos:")
for i, cnpj in enumerate(cnpjs):
    st.write(f"{i+1}. {cnpj}")
    if st.button(f"Excluir {cnpj}"):
        cnpjs.remove(cnpj)
        st.write(f"{cnpj} excluído com sucesso!")