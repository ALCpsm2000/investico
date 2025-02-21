import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import deque
from PIL import Image
import time
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go





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

logo = logo.resize((250, 250))  # Increase the size to 250x250 pixels

# Display the logo inside the sidebar
with st.sidebar:
    st.image(logo, width=250)  # Display the logo in the sidebar
    st.title("INVESTICO CAPITAL")  # Sidebar title

st.write("<h2 style='color: rgb(192, 79, 21);'>Nuestro Fondo</h2>", unsafe_allow_html=True)
st. write("Nustro Fondo tiene una parte Core, Pasive, y Hedged")


df = pd.read_excel("returns.xlsx")
df1 = pd.read_excel("assetallocation.xlsx")


df['Date'] = pd.to_datetime(df['Date'])

# Create the plot
fig = px.line(df, x='Date', y=['NAV Fund', 'NAV BM'], 
              title="NAV",
              labels={'Date': 'Date', 'value': 'NAV'},
              color_discrete_sequence=['#1f77b4', '#ff7f0e'])
# Customize hover data
fig.update_traces(marker=dict(size=8), hovertemplate="NAV: %{x}<br>Date: %{y}")

# Customize layout
fig.update_layout(
    plot_bgcolor="#f5f5f5",  # Set background color
    xaxis=dict(showgrid=True, gridcolor='white'),
    yaxis=dict(showgrid=True, gridcolor='white')
)

fig.update_layout(
    plot_bgcolor="#f5f5f5",  # Set plot background to light gray
    paper_bgcolor="#0E1117",  # Set paper (entire figure) background color
    title="NAV Fondo",  # Add title
    title_x=0.5,  # Center the title
    title_font=dict(
        size=24,  # Font size of the title
        family="Arial",  # Font family of the title
        color="white"  # Font color of the title
    ),
    legend=dict(title="Sectores",  # Set legend title
        font=dict(
            size=14,  # Font size for legend text
            color="white"  # Font color for legend text (main legend text)
        )))








fig1 = go.Figure(go.Pie(
    labels=df1['Sector'],  # Use the 'Sector' column for labels
    values=df1['Peso'],    # Use the 'Peso' column for values
    hole=0.4,             # Makes it a donut plot (hole in the center)
    marker=dict(colors=['#ff7f0e', '#1f77b4', '#2ca02c'])  # Custom colors
))

# Customize the background color
fig1.update_layout(
    plot_bgcolor="#f5f5f5",  # Set plot background to light gray
    paper_bgcolor="#0E1117",  # Set paper (entire figure) background color
    title="Asset Allocation ",  # Add title
    title_x=0.5,  # Center the title
    title_font=dict(
        size=24,  # Font size of the title
        family="Arial",  # Font family of the title
        color="white"  # Font color of the title
    ),
    legend=dict(title="Sectores",  # Set legend title
        font=dict(
            size=14,  # Font size for legend text
            color="white"  # Font color for legend text (main legend text)
        )))


# Display the plot in Streamlit
st.plotly_chart(fig1)

# Show the plot in Streamlit
st.plotly_chart(fig)





st.write("Here's the DataFrame:", df)