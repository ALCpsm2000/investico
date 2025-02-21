import streamlit as st
from PIL import Image

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

st.title("Nuestra Filosofia")