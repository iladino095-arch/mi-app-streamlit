import streamlit as st
import pandas as pd
import numpy as np

# 1. Configuración de la página
st.set_page_config(
    page_title="Control de Rendimiento de Labores",
    page_icon="👥",
    layout="wide"
)

st.title("📊 Control de Rendimiento y Labores en Cultivo")
st.write("Panel operativo para la supervisión de eficiencias, cumplimiento de metas y asignación de personal.")

# 2. Simulación de base de datos de labores (Sustituible por Excel, CSV o Supabase)
@st.cache_data
def cargar_rendimientos():
    data = [
        {"Operario": "Carlos Pérez", "Labor": "Corte", "Camas_Asignadas": 28, "Horas_Trabajadas": 8, "Produccion_Real_Total": 3120, "Meta_Hora": 390},
        {"Operario": "Ana Gómez", "Labor": "Corte", "Camas_Asignadas": 28, "Horas_Trabajadas": 8, "Produccion_Real_Total": 3400, "Meta_Hora": 390},
        {"Operario": "Luis Torres", "Labor": "Desbotone", "Camas_Asignadas": 30, "Horas_Trabajadas": 8, "Produccion_Real_Total": 45, "Meta_Hora": 40}, # Minutos por cama invertidos
        {"Operario": "María Ruiz", "Labor": "Deshierbe", "Camas_Asignadas": 28, "Horas_Trabajadas": 4, "Produccion_Real_Total": 3.5, "Meta_Hora": 4}, # Horas reales
        {"Operario": "Jorge Castro", "Labor": "Balance Foliar", "Camas_Asignadas": 28, "Horas_Trabajadas": 6, "Produccion_Real_Total": 25, "Meta_Hora": 30} # Minutos por cama
    ]
    return pd.DataFrame(data)

df = cargar_rendimientos()

# 3. Filtros en la barra lateral
st.sidebar.header("Filtros de Análisis")
labor_filtro = st.sidebar.selectbox("Filtrar por Labor:", ["Todas"] + list(df['Labor'].unique()))

if labor_filtro != "Todas":
    df_filtrado = df[df['Labor'] == labor_filtro].copy()
else:
    df_filtrado = df.copy()

# 4. Métricas Generales del Personal
st.subheader("📌 Indicadores Globales")
col1, col2, col3 = st.columns(3)

col1.metric("Personal Evaluado", f"{len(df_filtrado)} trabajadores")
col2.metric("Promedio Camas Asignadas", f"{df_filtrado['Camas_Asignadas'].mean():.1f} camas")
col3.metric("Labores Registradas", len(df_filtrado))

st.markdown("---")

# 5. Visualización detallada de la tabla
st.subheader("📋 Detalle de Rendimientos por Operario")
st.dataframe(df_filtrado, use_container_width=True)

# 6. Sección Interactiva: Registrar o simular evaluación de un operario
st.markdown("---")
st.subheader("✍️ Registro o Evaluación de Nueva Labor")

with st.form("form_labor"):
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        nombre_op = st.text_input("Nombre del Operario", "Ej. Juan Rodríguez")
        tipo_labor = st.selectbox("Tipo de Labor", ["Corte", "Desbotone", "Deshierbe", "Balance Foliar"])
    with col_f2:
        camas_asignadas = st.number_input("Camas Asignadas", min_value=1, max_value=40, value=28)
        horas_trabajadas = st.number_input("Horas Trabajadas", min_value=1.0, max_value=12.0, value=8.0)
    with col_f3:
        produccion_total = st.number_input("Cantidad Producida / Tiempo Total", value=3000.0)
        
    btn_evaluar = st.form_submit_button("Calcular Eficiencia")
    
    if btn_evaluar:
        st.success(f"Evaluación procesada exitosamente para **{nombre_op}** en la labor de **{tipo_labor}**.")
        if tipo_labor == "Corte":
            rendimiento_hora = produccion_total / horas_trabajadas
            st.info(f"Rendimiento obtenido: **{rendimiento_hora:.1f} tallos/hora** (Meta mínima esperada: 390 tallos/h).")
            if rendimiento_hora >= 390:
                st.balloons()
                st.write("✅ **¡Cumple con el estándar de rendimiento!**")
            else:
                st.warning("⚠️ **Por debajo del rendimiento mínimo esperado.** Requiere revisión de soporte en bloque.")

# 7. Opción de carga de archivo real (Excel) por parte del usuario
st.markdown("---")
st.subheader("📁 ¿Prefieres subir tu propio reporte de Excel?")
archivo_excel = st.file_uploader("Sube tu archivo de control de labores (.xlsx)", type=["xlsx"])

if archivo_excel is not None:
    df_usuario = pd.read_excel(archivo_excel)
    st.success("¡Archivo cargado y procesado correctamente desde tu equipo!")
    st.dataframe(df_usuario)
