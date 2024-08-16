import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np


def analise_visitas(df):
    st.title("Análise de Visitas e Status")

    df['DATA PARA VISITA'] = pd.to_datetime(df['DATA PARA VISITA'], errors='coerce')

    df['MÊS'] = df['DATA PARA VISITA'].dt.to_period('M').astype(str)

    visitas_por_mes = df['MÊS'].value_counts().sort_index()

    status_concluidos = df[df['STATUS'] == 'CONCLUÍDO']['MÊS'].value_counts().sort_index()

    fig_visitas = px.bar(visitas_por_mes,
                         x=visitas_por_mes.index,
                         y=visitas_por_mes.values,
                         labels={'x': 'Mês', 'y': 'Número de Visitas'},
                         title='Número de Visitas por Mês',
                         color=visitas_por_mes.values,
                         color_continuous_scale=px.colors.sequential.Greens)
    st.plotly_chart(fig_visitas)

    fig_concluidos = px.bar(status_concluidos,
                            x=status_concluidos.index,
                            y=status_concluidos.values,
                            labels={'x': 'Mês', 'y': 'Número de Status Concluídos'},
                            title='Número de Status Concluídos por Mês',
                            color=status_concluidos.values,
                            color_continuous_scale=px.colors.sequential.Greens)
    st.plotly_chart(fig_concluidos)

    fig, ax = plt.subplots()

    meses = pd.to_datetime(visitas_por_mes.index).strftime('%b %Y')
    ax.scatter(meses, visitas_por_mes.values, color='#2E8B57', edgecolor='black')
    ax.set_xticklabels(meses, rotation=45, ha='right')
    ax.set_title('Visitas por Mês')
    ax.set_xlabel('Mês')
    ax.set_ylabel('Número de Visitas')

    st.pyplot(fig)

    st.write("Análise concluída. Explore os gráficos acima para obter mais insights!")
