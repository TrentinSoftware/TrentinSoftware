import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode


def adicionar_linha(df):
    st.subheader("Adicionar Nova Linha")

    with st.form(key='form_adicionar_linha'):
        novas_colunas = {col: st.text_input(f"{col}:") for col in df.columns}
        submit_button = st.form_submit_button(label='Adicionar Linha')

        if submit_button:
            nova_linha = {col: novas_colunas[col] for col in df.columns}
            df = pd.concat([df, pd.DataFrame([nova_linha], columns=df.columns)], ignore_index=True)
            st.success("Linha adicionada com sucesso!")
            st.experimental_rerun()  # Recarrega a página para atualizar a tabela

    return df


def alterar_planilha(df):
    df = adicionar_linha(df)

    # Configurações do Grid
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(editable=True, filterable=True, sortable=True)
    grid_options = gb.build()

    grid_response = AgGrid(
        df,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.MANUAL,
        enable_enterprise_modules=True,
        theme='streamlit',
        fit_columns_on_grid_load=True
    )

    df_modificado = pd.DataFrame(grid_response['data'])

    if st.button("Salvar Alterações"):
        df_modificado.to_excel(r'C:\Users\LAB-F3-PC13\Documents\uas.xlsx', sheet_name='Planilha1', index=False)
        st.success("Alterações salvas com sucesso!")

    return df_modificado
