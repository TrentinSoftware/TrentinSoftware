import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode

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


def prox_compromisso(df):
    # Cria uma cópia do DataFrame para evitar alterações no DataFrame original
    df_copy = df.copy()

    # Certifique-se de que a coluna "DATA PARA VISITA" esteja no formato datetime
    df_copy['DATA PARA VISITA'] = pd.to_datetime(df_copy['DATA PARA VISITA'], errors='coerce')

    # Filtra as datas futuras (a partir do dia de hoje)
    hoje = datetime.now()
    df_futuras = df_copy[df_copy['DATA PARA VISITA'] >= hoje]

    # Ordena as datas futuras e seleciona as 3 mais próximas
    datas_proximas = df_futuras.sort_values(by='DATA PARA VISITA').head(3)

    # Exibe as datas
    if not datas_proximas.empty:
        st.subheader("Datas de visitas mais próximas")
        for index, row in datas_proximas.iterrows():
            st.write(f"- {row['DATA PARA VISITA'].strftime('%d/%m/%Y')}")
    else:
        st.write("Nenhuma data futura encontrada.")


def exibir_tabela(df, path_df, sheet_name):
    st.markdown("<h2 style='text-align: center;'>Como está cada Agência?</h2>", unsafe_allow_html=True)

    # Forçar a coluna "COD UA" a ser tratada como texto
    if 'COD UA' in df.columns:
        df['COD UA'] = df['COD UA'].astype(str)

    # Filtros
    status_options = df['STATUS'].unique().tolist()
    nome_ua_options = df['NOME UA'].unique().tolist()
    status_selecionado = st.selectbox('Filtrar por status:', ['Todos'] + status_options)
    nome_ua_selecionado = st.multiselect('Filtrar por NOME UA:', nome_ua_options)

    if status_selecionado != 'Todos':
        df = df[df['STATUS'] == status_selecionado]

    if nome_ua_selecionado:
        df = df[df['NOME UA'].isin(nome_ua_selecionado)]

    # Adiciona uma linha vazia para novos registros
    nova_linha = pd.DataFrame({col: [''] for col in df.columns}, index=[len(df)])
    df = pd.concat([df, nova_linha], ignore_index=True)

    # Configurações do AgGrid
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(editable=True, filterable=True, sortable=True)

    opcoes_status = ["PENDENTE", "CONCLUÍDO", "EM ANDAMENTO"]
    gb.configure_column("STATUS", editable=True, cellEditor="agSelectCellEditor",
                        cellEditorParams={"values": opcoes_status})

    gb.configure_grid_options(
        enableRangeSelection=True,
        suppressRowClickSelection=True,
        rowSelection='single',
        pagination=False,  # Desabilita paginação para visualização contínua
        enableCellTextSelection=True,
        suppressMenuHide=True
    )
    grid_options = gb.build()

    # Exibe a tabela com edição direta habilitada
    grid_response = AgGrid(
        df,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.MODEL_CHANGED,  # Usa modelo alterado para detecção
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        enable_enterprise_modules=True,
        theme='streamlit',
        fit_columns_on_grid_load=True
    )

    df_modificado = pd.DataFrame(grid_response['data'])

    if not df.equals(df_modificado):
        # Forçar a coluna "COD UA" a ser salva como texto
        if 'COD UA' in df_modificado.columns:
            df_modificado['COD UA'] = df_modificado['COD UA'].astype(str)
        df_modificado.to_excel(path_df, sheet_name=sheet_name, index=False)
        st.success("Alterações salvas automaticamente!")