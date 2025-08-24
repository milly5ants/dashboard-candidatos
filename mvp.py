import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# Título
st.title("📊 Dashboard de Candidatos")

# Carregar planilha LOCAL
#df_candidatos = pd.read_excel('candidatos.xlsx')

# Carregar planilha URL google sheet

sheet_url = "https://docs.google.com/spreadsheets/d/1252quJLdPfX0sgkQiByVz-1tJurycH3nl5Hh28JIXvQ/edit?usp=sharing"
csv_url = sheet_url.replace("/edit?usp=sharing", "/export?format=csv&gid=0")

df_candidatos = pd.read_csv(csv_url)

# Filtros
cidades = st.multiselect(
    "Selecione as cidades", 
    df_candidatos["Cidade"].unique(), 
    default=df_candidatos["Cidade"].unique()
)

profissoes = st.multiselect(
    "Selecione as profissões", 
    df_candidatos["Profissão"].unique(), 
    default=df_candidatos["Profissão"].unique()
)

# Aplicar filtros
df_filtrado = df_candidatos[
    (df_candidatos["Cidade"].isin(cidades)) & 
    (df_candidatos["Profissão"].isin(profissoes))
]

# Contador de candidatos filtrados
st.metric("Total de Candidatos Filtrados", len(df_filtrado))

# Tabela filtrada
st.subheader("📋 Tabela de Candidatos Filtrada")
st.dataframe(df_filtrado)

# Função para exportar Excel
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Candidatos')
    writer.close()
    return output.getvalue()

# Botão de download
st.download_button(
    label="📥 Baixar Excel",
    data=to_excel(df_filtrado),
    file_name="candidatos_filtrados.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Gráficos lado a lado
col1, col2 = st.columns(2)

with col1:
    st.subheader("📌 Distribuição por Profissão")
    fig = px.bar(
        df_filtrado, 
        y="Profissão", 
        color="Profissão", 
        title="Candidatos por Profissão", 
        text_auto=True,
        orientation='h'
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📌 Distribuição por Cidade")
    fig2 = px.bar(
        df_filtrado, 
        x="Cidade", 
        color="Cidade", 
        title="Candidatos por Cidade", 
        text_auto=True
    )
    st.plotly_chart(fig2, use_container_width=True)
