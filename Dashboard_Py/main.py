import streamlit as st
import pandas as pd
from first_page import graf_pizza, exibir_tabela
from register_page import alterar_planilha

def pagina_inicial(df):
    graf_pizza(df)
    exibir_tabela(df)

def segunda_pagina(df):
    st.title("Página de Cadastro")
    alterar_planilha(df)

file_path = r'C:\Users\LAB-F3-PC13\Documents\uas.xlsx'
df = pd.read_excel(file_path, sheet_name='Planilha1')

pagina = st.sidebar.selectbox(
    "Navegação",
    ("Página Inicial", "Página de Cadastro",)
)

# Lógica para exibir a página selecionada
if pagina == "Página Inicial":
    pagina_inicial(df)
elif pagina == "Página de Cadastro":
    segunda_pagina(df)