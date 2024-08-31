import streamlit as st
import pandas as pd
from first_page import graf_pizza, exibir_tabela, prox_compromisso
from analytic_page import analise_visitas
import base64

def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")
def pagina_inicial(df,file_path,sheet_name):
    graf_pizza(df)
    prox_compromisso(df)
    exibir_tabela(df=df,path_df=file_path,sheet_name=sheet_name)

def segunda_pagina(df):
    analise_visitas(df)

file_path = r'C:\Users\LAB-F3-PC13\Documents\uas.xlsx'
sheet_name = 'Planilha1'
df = pd.read_excel(file_path, sheet_name=sheet_name)

logo_path = r'C:\Users\LAB-F3-PC13\Documents\sicredi-160.png'
st.markdown(
    f"""
    <div style="display: flex; justify-content: center; align-items: center;">
        <h1 style="margin-bottom: 0;"></h1>
        <img src="data:image/png;base64,{image_to_base64(logo_path)}" alt="Logo" width="240" style="float: right; margin-right: 20px;">
    </div>
    """,
    unsafe_allow_html=True
)

pagina = st.sidebar.selectbox(
    "Navegação",
    ("Acompanhamento Agência Sustentável", "Analítico detalhado",)
)

# Lógica para exibir a página selecionada
if pagina == "Acompanhamento Agência Sustentável":
    pagina_inicial(df=df,file_path=file_path,sheet_name=sheet_name)
elif pagina == "Analítico detalhado":
    segunda_pagina(df=df)