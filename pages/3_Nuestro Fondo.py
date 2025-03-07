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
st.set_page_config(page_title="Investico", layout="wide")

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


df = pd.read_excel("returns.xlsx")
df1 = pd.read_excel("assetallocation.xlsx")
df0 = pd.read_excel("strategyallocation.xlsx")



#RETURN CALCULATOR

def calculate_final_quantity(df, start_date, initial_quantity):
    """
    Calculates the final quantity given an initial quantity and a start date.
    
    Parameters:
        df (pd.DataFrame): DataFrame with 'date' (datetime) and 'returns' columns.
        start_date (str or datetime): The start date for calculating returns.
        initial_quantity (float): The initial quantity to be adjusted by returns.

    Returns:
        float: The final quantity after applying returns.
    """
    # Ensure date column is datetime
    df["Date"] = pd.to_datetime(df['Date'])

    # Filter the DataFrame from the start_date onward
    df_filtered = df[df["Date"] >= pd.to_datetime(start_date)]

    # Calculate the cumulative product of returns
    total_return = df_filtered["Fund_1"].prod()

    # Compute final quantity
    final_quantity = initial_quantity * total_return

    return final_quantity


st.title("Nuestro Fondo 📈")

st.write("<h2 style='color: rgb(192, 79, 21);'>Calculadora de inversión</h2>", unsafe_allow_html=True)
start_date = st.date_input("Select Start Date", df["Date"].min(), max_value=df["Date"].max())
initial_quantity = st.number_input("Enter Initial Quantity", min_value=0.0, value=100.0, step=10.0)

if st.button("Calculate"):
    result = calculate_final_quantity(df, start_date, initial_quantity)
    st.write(f"Cantidad a dia de hoy: **{result:.2f}**")










# Load the logo from the same folder
logo = Image.open("logo.png")  # The logo file should be named 'logo.png' and in the same folder

logo = logo.resize((250, 250))  # Increase the size to 250x250 pixels

# Display the logo inside the sidebar
with st.sidebar:
    st.image(logo, width=250)  # Display the logo in the sidebar
    st.title("INVESTICO CAPITAL")  # Sidebar title

st.sidebar.write("Rentabilidad desde inicio:")
st.sidebar.write("Fondo: -0.74%")
st.sidebar.write("BM: -1.29%")
st.sidebar.write("")
st.sidebar.write("Estrategias:")
st.sidebar.write("Core: -1.77%")
st.sidebar.write("Pasiva: -0,56%")
st.sidebar.write("Hedge: 4,18%")





st.write("<h2 style='color: rgb(192, 79, 21);'>Nuestro Fondo</h2>", unsafe_allow_html=True)
st. write("Nustro Fondo esta compuesto de Core, Pasive, y Hedged")



df['Date'] = pd.to_datetime(df['Date'])

# Create the plot
fig = px.line(df, x='Date', y=['NAV Fund', 'NAV BM'], 
              title="NAV",
              labels={'Date': 'Date', 'value': 'NAV'},
              color_discrete_sequence=['#1f77b4', '#ff7f0e'])
# Customize hover data
fig.update_traces(marker=dict(size=8), hovertemplate="Date: %{x}<br>NAV: %{y}")


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


fig.update_layout(
    plot_bgcolor="#f5f5f5",  # Set background color
    xaxis=dict(showgrid=True, gridcolor='white'),
    yaxis=dict(showgrid=True, gridcolor='white', range=[95, 105])  # Force y-axis range
)




#asset allocation by strategies
fig0 = go.Figure(go.Pie(
    labels=df0['Estrategia'],  # Use the 'Sector' column for labels
    values=df0['Peso'],    # Use the 'Peso' column for values
    hole=0.4,             # Makes it a donut plot (hole in the center)
    marker=dict(colors=['rgb(192,79,21))', 'rgb(8,79,106)', 'rgb(39,83,23)',"rgb(10,105,135)"])  # Custom colors
))

fig0.update_layout(
    plot_bgcolor="#f5f5f5",  # Set plot background to light gray
    paper_bgcolor="#0E1117",  # Set paper (entire figure) background color
    title="Estrategia ",  # Add title
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










#big pie
fig1 = go.Figure(go.Pie(
    labels=df1['Sector'],  # Use the 'Sector' column for labels
    values=df1['Peso'],    # Use the 'Peso' column for values
    hole=0.4,             # Makes it a donut plot (hole in the center)
    marker=dict(colors=['rgb(192,79,21))', 'rgb(8,79,106)', 'rgb(39,83,23)',"rgb(220,105,50)","rgb(10,105,135)","rgb(50,110,30)","rgb(170,60,15)","rgb(5,60,90)","rgb(25,100,40)","rgb(180,70,25","rgb(210,90,40)","rgb(20,70,110)"])  # Custom colors
))

# Customize the background color
fig1.update_layout(
    plot_bgcolor="#f5f5f5",  # Set plot background to light gray
    paper_bgcolor="#0E1117",  # Set paper (entire figure) background color
    title="Asset Allocation Estrategia CORE ",  # Add title
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


#active return chart
fig3 = px.line(df, x='Date', y=['Active'], 
              title="Active Return",
              labels={'Date': 'Date', 'value': 'Active return'},
              color_discrete_sequence=['#1f77b4', '#ff7f0e'])


fig3.update_layout(
    plot_bgcolor="#f5f5f5",  # Set plot background to light gray
    paper_bgcolor="#0E1117",  # Set paper (entire figure) background color
    title="Active return",  # Add title
    title_x=0.5,  # Center the title
    title_font=dict(
        size=24,  # Font size of the title
        family="Arial",  # Font family of the title
        color="white"  # Font color of the title
    ),
    legend=dict(title="",  # Set legend title
        font=dict(
            size=14,  # Font size for legend text
            color="white"  # Font color for legend text (main legend text)
        )))








st.plotly_chart(fig0)
# Display the plot in Streamlit
st.plotly_chart(fig1)



# Show the plot in Streamlit
st.plotly_chart(fig)

st.plotly_chart(fig3)



#st.write("Here's the DataFrame:", df)
