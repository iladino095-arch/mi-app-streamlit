import streamlit as st
import pandas as pd
import numpy as np

# 1. Configuración general de la página
st.set_page_config(
    page_title="Monitoreo y Alertas Fitosanitarias",
    page_icon="🌱",
    layout="wide"
)

# Estilo visual limpio y profesional
st.markdown("""
    <style>
    .main-header { font-size: 24px; font-weight: bold; color: #2E7D32; }
    .metric-card { background-color: #f4f6f8; padding: 15px; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🌱 Sistema de Control Climático e Índice de Botrytis</p>', unsafe_allow_html=True)
st.write("Panel operativo para la supervisión de microclima y detección temprana de riesgos en bloques de producción.")

# 2. Simulación de carga de datos (Sustituible por conexión a Supabase)
@st.cache_data
def cargar_datos_sensores():
    np.random.seed(42)
    fechas = pd.date_range(start='2026-10-01 06:00:00', periods=48, freq='H')
    bloques = ['Bloque Alstroemeria 1', 'Bloque Alstroemeria 2', 'Bloque Rosas 1']
    
    data = []
    for fecha in fechas:
        for bloque in bloques:
            temp = round(np.random.uniform(11.0, 23.0), 1)
            hum = round(np.random.uniform(70.0, 95.0), 1)
            
            # Lógica de alerta crítica: Humedad >= 85% y Temperatura entre 12°C y 20°C
            alerta_botrytis = 1 if (hum >= 85) and (12 <= temp <= 20) else 0
            
            data.append({
                'Fecha_Hora': fecha,
                'Bloque': bloque,
                'Temperatura': temp,
                'Humedad': hum,
                'Alerta_Botrytis': alerta_botrytis
            })
            
    return pd.DataFrame(data)

df = cargar_datos_sensores()

# 3. Barra lateral de control y filtros
st.sidebar.header("Panel de Control")
bloque_seleccionado = st.sidebar.selectbox("Seleccione el Bloque:", df['Bloque'].unique())

# Filtrar datos según selección
df_filtrado = df[df['Bloque'] == bloque_seleccionado]

# 4. Métricas clave (KPIs) en la parte superior
col1, col2, col3 = st.columns(3)

temp_prom = df_filtrado['Temperatura'].mean()
hum_prom = df_filtrado['Humedad'].mean()
total_alertas = df_filtrado['Alerta_Botrytis'].sum()

col1.metric("Temperatura Promedio", f"{temp_prom:.1f} °C")
col2.metric("Humedad Relativa Prom.", f"{hum_prom:.1f} %")
col3.metric("Alertas de Botrytis", f"{total_alertas} registros", delta_color="inverse" if total_alertas > 0 else "off")

st.markdown("---")

# 5. Visualización gráfica de variables climáticas
st.subheader(f"Comportamiento Microclimático - {bloque_seleccionado}")

tab1, tab2 = st.tabs(["Gráfica de Tendencia", "Tabla de Datos Crudos"])

with tab1:
    # Gráfica combinada de Temperatura y Humedad
    st.line_chart(df_filtrado.set_index('Fecha_Hora')[['Temperatura', 'Humedad']])
    
    if total_alertas > 0:
        st.warning(f"⚠️ Atención: Se detectaron {total_alertas} momentos con condiciones de alto riesgo para desarrollo de *Botrytis* (Hum $\\ge$ 85% y Temp entre 12-20°C).")
    else:
        st.success("✅ Sin alertas críticas de riesgo fitosanitario en este bloque.")

with tab2:
    st.dataframe(df_filtrado, use_container_width=True)
    
    # Botón para descargar el reporte filtrado en CSV
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar reporte en CSV",
        data=csv,
        file_name=f'reporte_{bloque_seleccionado.lower().replace(" ", "_")}.csv',
        mime='text/csv',
    )

# 6. Formulario interactivo para simular ingreso manual de datos en campo
st.markdown("---")
st.subheader("📝 Registro Manual de Campo o Calibración")

with st.form("form_campo"):
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        temp_ingresada = st.number_input("Temperatura registrada (°C)", value=18.5)
    with col_f2:
        hum_ingresada = st.number_input("Humedad registrada (%)", value=88.0)
        
    btn_guardar = st.form_submit_button("Validar y Registrar Datos")
    
    if btn_guardar:
        # Evaluación rápida de la regla de negocio
        if hum_ingresada >= 85 and (12 <= temp_ingresada <= 20):
            st.error("🚨 ¡Alerta generada! Las condiciones ingresadas favorecen el desarrollo de hongos. Se recomienda aplicación preventiva.")
        else:
            st.success("✔️️ Condiciones estables. Sin riesgo inminente registrado en este punto.")
