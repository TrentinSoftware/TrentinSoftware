import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def graf_pizza(df):
    # Gráfico de Pizza para a coluna STATUS
    st.markdown("<h1 style='text-align: center;'>Projeto Agência Sustentável</h1>", unsafe_allow_html=True)
    status_counts = df['STATUS'].value_counts()

    colors = {
        'PENDENTE': '#808895',
        'CONCLUÍDO': '#64e164',
        'EM ANDAMENTO': '#3a98e1'
    }
    segment_colors = [colors.get(status, 'grey') for status in status_counts.index]

    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(
        status_counts,
        labels=[f'{label} ({count})' for label, count in zip(status_counts.index, status_counts)],
        autopct='%1.1f%%',
        colors=segment_colors,
        wedgeprops={'edgecolor': 'black', 'linewidth': 0.5}  # Define a cor da borda dos segmentos
    )

    for autotext in autotexts:
        autotext.set_color('white')

    st.pyplot(fig)

def exibir_tabela(df):
    # Título da tabela
    st.markdown("<h2 style='text-align: center;'>Como estão cada Agência?</h2>", unsafe_allow_html=True)

    status_options = df['STATUS'].unique().tolist()
    nome_ua_options = df['NOME UA'].unique().tolist()
    status_selecionado = st.selectbox('Filtrar por status:', ['Todos'] + status_options)
    nome_ua_selecionado = st.multiselect('Filtrar por NOME UA:', nome_ua_options)

    if status_selecionado != 'Todos':
        df = df[df['STATUS'] == status_selecionado]

    # Filtrar por NOME UA apenas se algo for selecionado
    if nome_ua_selecionado:
        df = df[df['NOME UA'].isin(nome_ua_selecionado)]

    def colorir_colunas(s):
        return ['background-color: lightblue' if col == 'STATUS' else '' for col in s.index]

    def colorir_linhas(index):
        return ['background-color: #f7f7f7' if index % 2 == 0 else 'background-color: #e7e7e7'] * len(df.columns)

    styled_df = df.style.apply(colorir_colunas, axis=1).apply(lambda s: colorir_linhas(s.name), axis=1)

    st.dataframe(styled_df)