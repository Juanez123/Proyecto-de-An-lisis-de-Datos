import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar el archivo
datos = pd.read_csv('./data/datos.csv', sep=';', encoding='latin1')

# Hacer las columnas mayúsculas
datos.columns = datos.columns.str.upper()

# Quitar acentos
datos = datos.replace('Á','A', regex=True)
datos = datos.replace('É','E', regex=True)
datos = datos.replace('Í','I', regex=True)
datos = datos.replace('Ó','O', regex=True)
datos = datos.replace('Ú','U', regex=True)

# Convertir números
datos['NUMERADOR'] = pd.to_numeric(datos['NUMERADOR'], errors='coerce')
datos['AÑO'] = pd.to_numeric(datos['AÑO'], errors='coerce')

# Filtrar solo VIH y SIDA
vih_sida = datos[datos['EVENTO'].str.contains('VIH|SIDA', case=False, na=False)]

# Quitar los que no tienen casos
vih_sida = vih_sida[vih_sida['NUMERADOR'] > 0]

# Preparar datos
casos_por_anio = vih_sida.groupby('AÑO')['NUMERADOR'].sum().reset_index()
departamentos = sorted(vih_sida['TERRITORIO'].unique().tolist())

# Configurar página
st.set_page_config(page_title="VIH/SIDA", layout="wide")
st.title("Análisis de VIH/SIDA en Colombia")

# Mostrar números principales
col1, col2, col3 = st.columns(3)
col1.metric("Total de casos", int(vih_sida['NUMERADOR'].sum()))
col2.metric("Departamentos", len(departamentos))
col3.metric("Años", int(vih_sida['AÑO'].nunique()))

# Gráfico 1: Casos por año
st.subheader("Casos por año")
grafico1 = px.line(casos_por_anio, x="AÑO", y="NUMERADOR", markers=True)
grafico1.update_traces(line=dict(color="#FF0066"), marker=dict(color="#FF0066"))
st.plotly_chart(grafico1, use_container_width=True)

# Gráfico 2: Casos por departamento
st.subheader("Casos por departamento")
depto = st.selectbox("Elige un departamento:", departamentos)
datos_depto = vih_sida[vih_sida['TERRITORIO'] == depto]

grafico2 = px.bar(datos_depto, x="AÑO", y="NUMERADOR")
grafico2.update_traces(marker=dict(color="#FF0066"))
st.plotly_chart(grafico2, use_container_width=True)

# Tabla
st.subheader("Todos los datos")
st.dataframe(vih_sida[['TERRITORIO', 'AÑO', 'EVENTO', 'NUMERADOR']])
