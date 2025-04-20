# app.py

import streamlit as st
import pandas as pd
from mplsoccer import Pitch
import matplotlib.pyplot as plt

# ===== Configurações Iniciais =====
st.set_page_config(page_title="Dashboard - Azuriz", layout="wide")

# ===== Sidebar: Filtros =====
st.sidebar.title("Filtros")

# Carregar banco de dados
@st.cache_data
def load_data():
    url = "https://drive.google.com/uc?id=1Qc-N2oHIhz-Mg5zoTN7jy6_QANUDMzQ4"
    df = pd.read_csv(url)
    return df

df = load_data()

# Filtros
categoria = st.sidebar.selectbox("Categoria", sorted(df['categoria'].dropna().unique()))
competicao = st.sidebar.selectbox("Competição", sorted(df['competição'].dropna().unique()))
jogo = st.sidebar.selectbox("Jogo", sorted((df['mandante'] + " x " + df['visitante']).dropna().unique()))
jogador = st.sidebar.multiselect("Jogador", sorted(df['jogador'].dropna().unique()))
metrica = st.sidebar.multiselect("Métrica", sorted(df['métrica'].dropna().unique()))

# Aplicar filtros
df_filtrado = df.copy()
if categoria:
    df_filtrado = df_filtrado[df_filtrado['categoria'] == categoria]
if competicao:
    df_filtrado = df_filtrado[df_filtrado['competição'] == competicao]
if jogo:
    mandante, visitante = jogo.split(" x ")
    df_filtrado = df_filtrado[(df_filtrado['mandante'] == mandante) & (df_filtrado['visitante'] == visitante)]
if jogador:
    df_filtrado = df_filtrado[df_filtrado['jogador'].isin(jogador)]
if metrica:
    df_filtrado = df_filtrado[df_filtrado['métrica'].isin(metrica)]

# ===== Tabs =====
tab1, tab2, tab3 = st.tabs(["📋 Tabela", "📈 Gráficos", "⚽ Campograma"])

with tab1:
    st.subheader("Tabela de Eventos")
    st.dataframe(df_filtrado)

with tab2:
    st.subheader("Gráficos de Métricas")
    # Aqui você pode colocar os gráficos que já fizemos: barras simples, empilhadas etc.
    if df_filtrado.empty:
        st.warning("Nenhum dado para gerar gráficos.")
    else:
        df_count = df_filtrado['jogador'].value_counts()
        st.bar_chart(df_count)

with tab3:
    st.subheader("Campogramas")
    if df_filtrado.empty:
        st.warning("Nenhum dado para gerar campograma.")
    else:
        pitch = Pitch(pitch_color='grass', line_color='white')
        fig, ax = pitch.draw(figsize=(10, 6))
        
        if 'xy' in df_filtrado.columns:
            df_xy = df_filtrado[df_filtrado['xy'].notna()]
            for _, row in df_xy.iterrows():
                try:
                    x, y = map(float, row['xy'].split(';'))
                    x = (x - 32) / (584 - 32) * 100
                    y = 100 - ((y - 14) / (375 - 14) * 100)
                    ax.scatter(x, y, color='red', edgecolor='black', s=80)
                    ax.text(x, y - 2, row['jogador'], fontsize=7, color='white', ha='center', va='top')
                except:
                    continue
        
        st.pyplot(fig)

