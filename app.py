import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuración de página
st.set_page_config(page_title="Analizador Derma CEI", layout="centered")

# Inyección de CSS (Fondo rosa general y letra grande forzada)
st.markdown("""
<style>
/* Fondo rosa para toda la aplicación */
.stApp {
    background-color: #fce4ec;
}
/* Forzar el tamaño de letra a 20px en los resultados del informe */
.resultado-gemini p, .resultado-gemini ul, .resultado-gemini li {
    font-size: 20px !important;
    color: #333333;
    line-height: 1.6;
}
/* Estilo del botón rosa */
div.stButton > button:first-child {
    background-color: #d81b60;
    color: white;
    border-radius: 20px;
    padding: 10px 24px;
    border: none;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Obtener clave secreta
try:
    GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
except:
    st.error("Falta configurar la llave de Google en los Secrets de Streamlit.")
    st.stop()

# --- CARGA DEL LOGO CEI ---
# Si subiste el archivo "logo.png" a GitHub, aparece acá arriba.
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        st.image("logo.png", use_container_width=True)
    except:
        pass # Si el logo no está subido, no tira error, simplemente sigue de largo.

# Interfaz de usuario
st.markdown("<h1 style='text-align: center; color: #d81b60; margin-top: -20px;'>ANALIZADOR DE PIEL</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #333333; font-weight: bold;'>Cargar rostro mediante:</p>", unsafe_allow_html=True)

opcion = st.radio("", ("Usar Cámara del Celu", "Subir de Galería"), horizontal=True)

imagen_cargada = None
if opcion == "Usar Cámara del Celu":
    imagen_cargada = st.camera_input("Sacá una foto de tu rostro")
else:
    imagen_cargada = st.file_uploader("Seleccioná una imagen de tu galería", type=['jpg', 'jpeg', 'png'])

if imagen_cargada is not None:
    imagen_pil = Image.open(imagen_cargada)
    
    if st.button("🚀 INICIAR DIAGNÓSTICO"):
        with st.spinner("Analizando tejido..."):
            try:
                # Motor V8 de Google
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # LA ORDEN ESTRICTA A LA IA
                prompt = """
                Actúa como un experto en cosmetología. Analiza esta imagen facial y determina ÚNICAMENTE:
                1. Biotipo cutáneo.
                2. Fototipo.
                3. Principales inesteticismos o condiciones visibles.
                IMPORTANTE: NO sugieras tratamientos, rutinas, ni nombres de principios activos. Tu tarea es exclusivamente el diagnóstico y análisis visual.
                Responde en español de Argentina, con un tono profesional, directo y claro.
                """
                
                response = model.generate_content([prompt, imagen_pil])
                
                # Recuadro blanco para que resalte sobre el fondo rosa, con la clase para agrandar la letra
                st.markdown(f"<div class='resultado-gemini' style='background-color: white; padding: 20px; border-radius: 15px; border-left: 5px solid #d81b60; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);'>{response.text}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"⚠️ Falla con Google: {str(e)}")

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray; font-size: 12px;'>Gestión Técnico-Analógica Internacional: Fabio & Olga — CEI 2026</p>", unsafe_allow_html=True)
