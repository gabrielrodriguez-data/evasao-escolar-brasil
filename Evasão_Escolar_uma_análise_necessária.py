import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração da página
st.set_page_config(page_title="Análise de Evasão Escolar", layout="wide")

# Configuração de estilo
sns.set_theme(style="whitegrid")
plt.rcParams["font.sans-serif"] = "Arial"
plt.rcParams["font.family"] = "sans-serif"

# Título do App
st.title("📊 Investigação Analítica: Evasão Escolar no Brasil")
st.markdown("Análise baseada em dados de 2018, 2020 e 2022.")

# --- Carga de Dados ---
@st.cache_data
def carregar_dados():
    url = "https://raw.githubusercontent.com/suzanasvm/visualizacao_de_dados/main/datasets/evasao_escolar_brasil.csv"
    df = pd.read_csv(url, sep=None, engine='python')
    df.columns = df.columns.str.strip()
    
    # Mapeamento
    colunas_mapeadas = {}
    for col in df.columns:
        c_norm = col.lower().replace("_", "")
        if "ano" in c_norm: colunas_mapeadas[col] = "Ano"
        elif "reg" in c_norm: colunas_mapeadas[col] = "Regiao"
        elif "evas" in c_norm: colunas_mapeadas[col] = "Taxa_Evasao"
        elif "inter" in c_norm or "net" in c_norm: colunas_mapeadas[col] = "Acesso_Internet_Pct"
    
    df = df.rename(columns=colunas_mapeadas)
    
    # Tratamento de tipos
    for col in ["Taxa_Evasao", "Acesso_Internet_Pct"]:
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.replace(',', '.').astype(float)
    return df

df = carregar_dados()

# --- Pergunta 1 ---
st.header("1. Resiliência Educacional (2018 vs 2022)")
df_comp = df[df["Ano"].isin([2018, 2022])].copy()
df_comp["Ano"] = df_comp["Ano"].astype(str)

fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.barplot(data=df_comp, x="Regiao", y="Taxa_Evasao", hue="Ano", palette={"2018": "#A8DADC", "2022": "#E63946"}, ax=ax1)
ax1.set_title("Evasão Escolar: 2018 vs 2022")
for container in ax1.containers:
    ax1.bar_label(container, fmt='%.1f%%')
sns.despine(left=True, bottom=True)
st.pyplot(fig1)

# --- Pergunta 2 ---
st.header("2. O Abismo Digital (2022)")
df_2022 = df[df["Ano"] == 2022].sort_values(by="Taxa_Evasao", ascending=False)

fig2, ax_bar = plt.subplots(figsize=(10, 5))
ax_bar.bar(df_2022["Regiao"], df_2022["Acesso_Internet_Pct"], color="#4A4E69", alpha=0.3, label="% Escolas com Internet")
ax_line = ax_bar.twinx()
ax_line.plot(df_2022["Regiao"], df_2022["Taxa_Evasao"], color="#E63946", marker="o", linewidth=3, label="Taxa de Evasão")
ax_bar.set_title("Conectividade vs Evasão em 2022")
ax_bar.set_ylabel("% Escolas com Internet")
ax_line.set_ylabel("Taxa de Evasão (%)")
st.pyplot(fig2)

st.success("Análise concluída com sucesso!")