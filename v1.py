import streamlit as st
import pandas as pd
from collections import deque
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



# Initialize session state for transactions if not already set
if "transactions" not in st.session_state:
    st.session_state.transactions = [
        {"Day": "09-12-2024", "BUY/SELL": "BUY", "Quantity": 5000, "Price": 100, "Total": 5000 * 100, "P&L": 0},
        {"Day": "20-12-2024", "BUY/SELL": "BUY", "Quantity": 5000, "Price": 110, "Total": 5000 * 110, "P&L": 0}
    ]
    st.session_state.fifo_queue = deque([(5000, 100), (5000, 110)])  # FIFO queue for cost tracking
    st.session_state.total_quantity = 10000  # Initial quantity held
    st.session_state.total_cost = (5000 * 100) + (5000 * 110)  # Initial total cost
    st.session_state.total_pnl = 0  # Initialize P&L
    st.session_state.current_price = 110  # Set fixed price

# Set dark theme only for background
st.markdown("""
    <style>
        body {
            background-color: #121212 !important;
            color: white !important;
        }
        .stApp {
            background-color: #121212 !important;
        }
        .dataframe tbody tr td {
            background-color: white !important;
            color: black !important;
        }
    </style>
    """, unsafe_allow_html=True)

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
    st.session_state.total_cost -= cost_removed

# Display portfolio summary
st.title("FIFO Trading Table")
st.subheader("Portfolio Summary")
st.write(f"**Quantity Held:** {st.session_state.total_quantity}")
st.write(f"**FIFO Cost:** {st.session_state.total_cost / max(1, st.session_state.total_quantity):.2f} per unit")
st.write(f"**Current Price:** {st.session_state.current_price}")
st.write(f"**Total P&L:** {st.session_state.total_pnl:.2f}")

# User input for transactions
st.subheader("New Transaction")
st.write("**Select Transaction Type:**")
quantity_input = st.number_input("Enter Quantity", min_value=1, value=1000)

col1, col2 = st.columns(2)
with col1:
    if st.button("Buy"):
        buy(quantity_input)
        st.rerun()

with col2:
    if st.button("Sell"):
        sell(quantity_input)
        st.rerun()

# Display transactions table
st.subheader("Transaction History")
df = pd.DataFrame(st.session_state.transactions)
st.table(df)
