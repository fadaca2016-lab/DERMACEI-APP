import streamlit as st
import requests
import base64

# 1. ESTÉTICA PROFESIONAL EN ROSA CEI
st.set_page_config(page_title="Derma CEI v11.0", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #fff0f5; }
    .stButton>button { 
        background-color: #d81b60; color: white; 
        border-radius: 20px; width: 100%; border: none; font-weight: bold; height: 3.5em;
    }
    .stButton>button:hover { background-color: #ff69b4; color: white; }
    h1, h2 { color: #d81b60; text-align: center; font-family: 'Helvetica Neue', Arial, sans-serif; }
    .stRadio > label { color: #ad1457; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>derma-cei</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#ad1457;'>Cosmiatra de Bolsillo - Canal Real Sin Claves</p>", unsafe_allow_html=True)
st.markdown("---")

# Función de visión real por canal libre (Inmune a los bloqueos de Google)
def analizar_foto_real_libre(campo_foto, prompt_texto):
    url = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-11B-Vision-Instruct"
    
    bytes_data = campo_foto.getvalue()
    base64_image = base64.b64encode(bytes_data).decode('utf-8')
    
    payload = {
        "inputs": f"<{prompt_texto}>\nData:image/jpeg;base64,{base64_image}",
        "parameters": {"max_new_tokens": 500}
    }
    
    try:
        # Le pega directo al servidor público sin pedir tokens de autorización
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            res_json = response.json()
            if isinstance(res_json, list) and len(res_json) > 0:
                return res_json[0].get('generated_text', '')
            elif isinstance(res_json, dict):
                return res_json.get('generated_text', '')
        return None
    except:
        return None

# 2. INTERFAZ OPERATIVA EXCLUSIVA (DIAGNÓSTICO CIENTÍFICO)
st.markdown("<h2>ANALIZADOR DE PIEL</h2>", unsafe_allow_html=True)
opcion = st.radio("Cargar rostro mediante:", ["📸 Usar Cámara del Celu", "🖼️ Subir de Galería"], horizontal=True)

foto = st.camera_input("Capturá el rostro") if opcion == "📸 Usar Cámara del Celu" else st.file_uploader("Seleccioná una imagen", type=['jpg', 'png', 'jpeg'])

if foto:
    if st.button("🚀 INICIAR DIAGNÓSTICO"):
        with st.spinner("Analizando el tejido real de la foto con Llama Vision..."):
            
            prompt = ("Actúa como un sistema avanzado de diagnóstico dermatocosmético para profesionales. "
                      "Analiza la piel de la imagen adjunta de forma científica. "
                      "Estructura tu respuesta usando exactamente estos títulos: "
                      "### 1) BIOTIPO CUTÁNEO (Describe detalladamente las zonas del rostro)\n\n"
                      "### 2) FOTOTIPO (Determina la Escala Fitzpatrick según los rasgos visibles)\n\n"
                      "### 3) CONDICIONES / LESIONES VISIBLES (Detalla líneas de expresión, manchas o sensibilidad sin sugerir marcas comerciales).")
            
            resultado = analizar_foto_real_libre(foto, prompt)
            
            if not resultado:
                st.error("⚠️ El canal libre está procesando muchas imágenes en este segundo. Esperá 10 segundos y volvé a presionar el botón rosa.")
            else:
                st.markdown(f"<div style='background-color: white; padding: 20px; border-radius: 15px; border-left: 5px solid #d81b60; color: black;'>{resultado}</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("Gestión Técnico-Analógica Internacional: CEI 2026")
