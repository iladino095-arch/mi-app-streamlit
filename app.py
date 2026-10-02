import streamlit as st

st.title("🌱 Mi Aplicación Operativa")
nombre = st.text_input("¿Cómo te llamas?")
if st.button("Saludar"):
    st.success(f"¡Hola, {nombre}! La app funciona perfecto.")
