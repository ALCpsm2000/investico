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

st.title("Nuestro Fondo")


# Load the logo from the same folder

if "first" not in st.session_state:
    st.session_state.first = True

if st.session_state.first:
    st.session_state.first = False
    place = st.empty()
    place.write("this is a loging page")
    if st.button("Click me"):
        st.write("INSIDE IF")
        
        time.sleep(10)
        place.empty()
    else:
        st.write("else")
        time.sleep(60)
    st.write("after while loop")




st.write("outside function")


st.rerun()










# Initialize session state for transactions if not already set
def initialize_session_state():
    if "transactions" not in st.session_state:
        st.session_state.transactions = [
            {"Day": "09-12-2024", "BUY/SELL": "BUY", "Quantity": 5000, "Price": 100, "Total": 5000 * 100, "P&L": 0},
            {"Day": "20-12-2024", "BUY/SELL": "BUY", "Quantity": 5000, "Price": 110, "Total": 5000 * 110, "P&L": 0}
        ]
        st.session_state.fifo_queue = deque([(5000, 100), (5000, 107)])  # FIFO queue for cost tracking
        st.session_state.total_quantity = 10000  # Initial quantity held
        st.session_state.total_cost = (5000 * 100) + (5000 * 110)  # Initial total cost
        st.session_state.total_pnl = 0  # Initialize P&L
        st.session_state.current_price = 110  # Set fixed price

initialize_session_state()

# Transaction Functions (buy/sell)
def buy(quantity):
    price = st.session_state.current_price  # Hardcoded price
    st.session_state.transactions.append({
        "Day": pd.Timestamp.now().strftime("%d-%m-%Y"),
        "BUY/SELL": "BUY",
        "Quantity": quantity,
        "Price": price,
        "Total": quantity * price,
        "P&L": 0
    })
    st.session_state.fifo_queue.append((quantity, price))
    st.session_state.total_quantity += quantity
    st.session_state.total_cost += quantity * price

def sell(quantity):
    sell_price = st.session_state.current_price  # Hardcoded sell price
    if quantity > st.session_state.total_quantity:
        st.warning("Not enough quantity to sell!")
        return
    
    remaining_to_sell = quantity
    total_sale_value = quantity * sell_price
    cost_removed = 0
    
    while remaining_to_sell > 0 and st.session_state.fifo_queue:
        qty, price = st.session_state.fifo_queue.popleft()
        if qty <= remaining_to_sell:
            remaining_to_sell -= qty
            cost_removed += qty * price
        else:
            st.session_state.fifo_queue.appendleft((qty - remaining_to_sell, price))
            cost_removed += remaining_to_sell * price
            remaining_to_sell = 0
    
    pnl = total_sale_value - cost_removed
    st.session_state.total_pnl += pnl
    
    st.session_state.transactions.append({
        "Day": pd.Timestamp.now().strftime("%d-%m-%Y"),
        "BUY/SELL": "SELL",
        "Quantity": -quantity,
        "Price": sell_price,
        "Total": -total_sale_value,
        "P&L": pnl
    })
    
    st.session_state.total_quantity -= quantity
    st.session_state.total_cost -= cost_removed  # Correct total cost after sale

def render_table_as_image(df):
    """Generates a bigger and more readable image of the transactions table"""
    fig, ax = plt.subplots(figsize=(16, len(df) * 0.9 + 2), dpi=300)  # Increased size for clarity
    
    ax.axis('tight')
    ax.axis('off')
    
    # Create the table with extra padding
    table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')

    # Improve table spacing and font size
    table.auto_set_font_size(False)
    table.set_fontsize(18)  # Bigger font
    table.auto_set_column_width(col=list(range(len(df.columns))))  # Adjust column width
    
    # Add extra padding around cells
    for key, cell in table.get_celld().items():
        cell.set_height(0.12)  # Increased row height
        if key[0] == 0:  # Header row
            cell.set_fontsize(20)  # Bigger header font
            cell.set_facecolor("#DDDDDD")  # Light gray header
        else:
            cell.set_facecolor("white")  # White background for rows
            cell.set_edgecolor("black")

    # Save the table
    plt.savefig("table.png", bbox_inches='tight', dpi=300, transparent=True)
    
    # Open image and overlay on a dark background
    table_img = Image.open("table.png")
    bg = Image.new("RGB", (table_img.width + 80, table_img.height + 80), "#0E1117")  # More space
    bg.paste(table_img, (40, 40), table_img)  # Centered with padding

    # Save final image
    bg.save("table_final.png")
    return "table_final.png"

# Login Logic
usuario = st.text_input("Usuario:", value="usuario")  # Pre-fill "usuario" in the textbox
contraseña = st.text_input("Contraseña:", type="password")  # Password field
login_button = st.button("Login")

# Wait for login success before proceeding
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if login_button:
    if usuario == "ieb" and contraseña == "1234":
        st.session_state.logged_in = True
        st.rerun()  # Re-run to load the authorized section
    else:
        st.warning("Credenciales incorrectas. Inténtalo de nuevo.")  # Show warning for incorrect credentials

# Only proceed if logged in
if st.session_state.logged_in:
    initialize_session_state()

    # Display portfolio summary
    st.title("Area del Inversor")
    st.subheader("Portfolio Summary")
    st.write(f"**Cantidad:** {st.session_state.total_quantity:,.0f}")
    st.write(f"**NAV:** {st.session_state.current_price:,.2f}")
    st.write(f"**Valor de Mercado:** {(st.session_state.current_price * st.session_state.total_quantity):,.2f}")
    st.write(f"**Plusvalia:** {(st.session_state.current_price * st.session_state.total_quantity)-(st.session_state.total_cost / max(1, st.session_state.total_quantity) * st.session_state.total_quantity):,.2f}")

    # User input for transactions
    st.subheader("New Transaction")
    st.write("**Select Transaction Type:**")
    quantity_input = st.number_input("Enter Quantity", min_value=1, value=1000)

    col1, col2 = st.columns(2)
    with col1:
        st.write("Subscripcion:")
        if st.button("Subscripcion"):
            buy(quantity_input)

    with col2:
        st.write("Reembolso:")
        if st.button("Reembolso"):
            sell(quantity_input)

    # Generate and display table image
    st.subheader("Transaction History")
    df = pd.DataFrame(st.session_state.transactions)
    table_image_path = render_table_as_image(df)
    st.image(table_image_path, use_column_width=True)

    st.write(f"**FIFO Cost:** {st.session_state.total_cost / max(1, st.session_state.total_quantity):.2f} per unit")
    st.write(f"**P&L Realizado:** {st.session_state.total_pnl:.2f}")
