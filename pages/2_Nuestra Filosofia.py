import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import deque
from PIL import Image
import time


# Set up the page configuration
st.set_page_config(page_title="Dark Theme App", layout="wide")

# Apply custom dark theme styling
st.markdown(
    """
    <style>
        /* Main background color */
        body, .stApp {
            background-color: #0E1117 !important;
            color: white !important;
        }

        /* Hide the top white bar */
        header[data-testid="stHeader"] {
            background-color: #0E1117 !important;
        }

        /* Sidebar background and text color */
        [data-testid="stSidebar"], [data-testid="stSidebarContent"] {
            background-color: #161A23 !important;
            color: white !important;
            width: 350px !important;  /* Increase the width of the sidebar */
        }

        /* Make sidebar text white */
        [data-testid="stSidebar"] * {
            color: white !important;
        }

        /* Increase font size specifically for the 'IVC' page in sidebar */
        a[href*="IVC"] {
            font-size: 2.5em !important;  /* Make the font size bigger */
            font-weight: bold !important; /* Make it bold */
            color: #FFDD00 !important;    /* Optional: Make it standout with a different color */
        }

        /* Make the main title bigger */
        .stTitle {
            font-size: 3.5em !important;
        }

        /* Make the first st.write text bigger */
        .stMarkdown p:first-child {
            font-size: 1.5em !important;
        }

        /* Place the logo in the sidebar */
        .logo-container {
            position: relative;
            top: 20px;
            left: 20px;
            width: 100%;
            padding-bottom: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Load the logo from the same folder
logo = Image.open("logo.png")  # The logo file should be named 'logo.png' and in the same folder

# Resize the logo to a larger size
logo = logo.resize((250, 250))  # Increase the size to 250x250 pixels

# Display the logo inside the sidebar
with st.sidebar:
    st.image(logo, width=250)  # Display the logo in the sidebar
    st.title("INVESTICO CAPITAL")  # Sidebar title

st.write("<h2 style='color: rgb(192, 79, 21);'>Nuestra Filosofía de Inversión</h2>", unsafe_allow_html=True)

st.subheader("En Investico, creemos en la gestión activa para superar el S&P 500.")

with st.expander("📊 Análisis exhaustivo"):
    st.write(
        "Realizamos un análisis profundo y riguroso de cada empresa en la que invertimos. "
        "Evaluamos factores fundamentales como los estados financieros, la posición competitiva, "
        "la calidad del equipo directivo y las perspectivas de crecimiento futuro."
    )

with st.expander("📈 Diversificación inteligente"):
    st.write(
        "Mantenemos una cartera diversificada que nos permite mitigar riesgos y aprovechar oportunidades "
        "en diversos sectores y geografías. No obstante, cada inversión es seleccionada con cuidado para maximizar "
        "el potencial de rendimiento."
    )

with st.expander("🔄 Adaptabilidad y flexibilidad"):
    st.write(
        "Nos adaptamos rápidamente a los cambios en el mercado y ajustamos nuestra estrategia según sea necesario. "
        "Esta flexibilidad nos permite capitalizar oportunidades emergentes y gestionar eficazmente los riesgos."
    )

with st.expander("🚀 Innovación constante"):
    st.write(
        "Estamos comprometidos con la innovación y la mejora continua. Utilizamos tecnologías avanzadas y técnicas de "
        "análisis para identificar oportunidades de inversión que otros puedan pasar por alto."
    )

with st.expander("⏳ Enfoque a largo plazo"):
    st.write(
        "Aunque buscamos batir el índice a través de una gestión activa, mantenemos un enfoque a largo plazo. "
        "Creemos que la creación de valor sostenible para nuestros inversores se logra mediante la identificación "
        "y el apoyo a empresas con potencial de crecimiento a largo plazo."
    )

with st.expander("💡 Transparencia y responsabilidad"):
    st.write(
        "Mantenemos una comunicación abierta y transparente con nuestros inversores. Nos comprometemos a proporcionar "
        "informes claros y precisos sobre el desempeño de nuestra cartera y nuestras decisiones de inversión."
    )

st.write(
    "**Nuestra misión** es ofrecer a nuestros inversores rendimientos consistentes y superiores al índice, mientras "
    "gestionamos diligentemente los riesgos y buscamos oportunidades innovadoras en el mercado."
)

