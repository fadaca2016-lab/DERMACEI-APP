import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuración de página
st.set_page_config(page_title="Analizador Derma CEI", layout="centered")

# Obtener clave secreta
try:
    GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
except:
    st.error("Falta configurar la llave de Google en los Secrets de Streamlit.")
    st.stop()

# Interfaz de usuario
st.markdown("<h1 style='text-align: center; color: #333333;'>ANALIZADOR DE PIEL</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #d81b60;'>Cargar rostro mediante:</p>", unsafe_allow_html=True)

opcion = st.radio("", ("Usar Cámara del Celu", "Subir de Galería"), horizontal=True)

imagen_cargada = None
if opcion == "Usar Cámara del Celu":
    imagen_cargada = st.camera_input("Sacá una foto de tu rostro")
else:
    imagen_cargada = st.file_uploader("Seleccioná una imagen de tu galería", type=['jpg', 'jpeg', 'png'])

if imagen_cargada is not None:
    imagen_pil = Image.open(imagen_cargada)
    
    # Botón rosa
    st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #d81b60;
        color: white;
        border-radius: 20px;
        padding: 10px 24px;
        border: none;
        font-weight: bold;
    }
    </style>""", unsafe_allow_html=True)
    
    if st.button("🚀 INICIAR DIAGNÓSTICO"):
        with st.spinner("Analizando tejido..."):
            try:
                # Motor V8 de Google
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                prompt = """
                Actúa como un experto en cosmetología. Analiza esta imagen facial y determina:
                1. Biotipo cutáneo.
                2. Fototipo.
                3. Principales inesteticismos o condiciones visibles.
                4. Recomendación de principios activos (INCI) para tratamiento, sin mencionar marcas comerciales.
                Responde en español de Argentina, con un tono profesional pero directo y claro.
                """
                
                response = model.generate_content([prompt, imagen_pil])
                
                st.markdown(f"<div style='background-color: white; padding: 20px; border-radius: 15px; border-left: 5px solid #d81b60; color: black;'>{response.text}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"⚠️ Falla con Google: {str(e)}")

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray; font-size: 14px;'>Gestión Técnico-Analógica Internacional: — CEI 2026</p>", unsafe_allow_html=True)
