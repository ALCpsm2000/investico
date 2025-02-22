import streamlit as st
import pandas as pd
from collections import deque
from PIL import Image
import time

# Set up the page configuration
st.set_page_config(page_title="Dark Theme App", layout="wide")

# Apply custom dark theme styling
st.markdown(
    """
    <style>
        body, .stApp { background-color: #0E1117 !important; color: white !important; }
        header[data-testid="stHeader"] { background-color: #0E1117 !important; }
        [data-testid="stSidebar"], [data-testid="stSidebarContent"] {
            background-color: #161A23 !important; color: white !important; width: 350px !important;
        }
        [data-testid="stSidebar"] * { color: white !important; }
        a[href*="IVC"] { font-size: 2.5em !important; font-weight: bold !important; color: #FFDD00 !important; }
        .stTitle { font-size: 3.5em !important; }
        .stMarkdown p:first-child { font-size: 1.5em !important; }
    </style>
    """,
    unsafe_allow_html=True
)

# Load and display logo in sidebar
logo = Image.open("logo.png").resize((250, 250))
with st.sidebar:
    st.image(logo, width=250)
    st.title("INVESTICO CAPITAL")

st.write("<h2 style='color: rgb(192, 79, 21);'>Area Cliente</h2>", unsafe_allow_html=True)

# Login State Management
if "not_logged_in" not in st.session_state:
    st.session_state.not_logged_in = True
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.not_logged_in:
    username = st.text_input("Usuario")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "ieb" and password == "1234":
            st.success("You have successfully logged in")
            st.session_state.not_logged_in = False
            st.session_state.logged_in = True
            time.sleep(2)
            st.rerun()
        else:
            st.error("Invalid credentials. Please try again.")

# Initialize session state for transactions if not already set
def initialize_session_state():
    if "transactions_df" not in st.session_state:
        st.session_state.transactions_df = pd.DataFrame([
            {"Day": "09-12-2024", "BUY/SELL": "BUY", "Quantity": 5000, "Price": 100, "Total": 5000 * 100, "P&L": 0},
            {"Day": "20-12-2024", "BUY/SELL": "BUY", "Quantity": 5000, "Price": 110, "Total": 5000 * 110, "P&L": 0}
        ])
        st.session_state.fifo_queue = deque([(5000, 100), (5000, 110)])
        st.session_state.total_quantity = 10000
        st.session_state.total_cost = (5000 * 100) + (5000 * 110)
        st.session_state.total_pnl = 0
        st.session_state.current_price = 110

if st.session_state.logged_in:
    initialize_session_state()

    # Portfolio Summary
    st.title("Area del Inversor")
    st.subheader("Portfolio Summary")
    st.write(f"**Cantidad:** {st.session_state.total_quantity:,.0f}")
    st.write(f"**NAV:** {st.session_state.current_price:,.2f}")
    st.write(f"**Valor de Mercado:** {(st.session_state.current_price * st.session_state.total_quantity):,.2f}")
    st.write(f"**Plusvalia:** {(st.session_state.current_price * st.session_state.total_quantity) - (st.session_state.total_cost / max(1, st.session_state.total_quantity) * st.session_state.total_quantity):,.2f}")

    # Transaction Functions
    def buy(quantity):
        price = st.session_state.current_price
        new_transaction = {"Day": pd.Timestamp.now().strftime("%d-%m-%Y"), "BUY/SELL": "BUY", "Quantity": quantity, "Price": price, "Total": quantity * price, "P&L": 0}
        st.session_state.transactions_df = pd.concat([st.session_state.transactions_df, pd.DataFrame([new_transaction])], ignore_index=True)
        st.session_state.fifo_queue.append((quantity, price))
        st.session_state.total_quantity += quantity
        st.session_state.total_cost += quantity * price

    def sell(quantity):
        sell_price = st.session_state.current_price
        if quantity > st.session_state.total_quantity:
            st.warning("Not enough quantity to sell!")
            return
        
        st.session_state.total_quantity -= quantity
        st.session_state.transactions_df = pd.concat([st.session_state.transactions_df, pd.DataFrame([{"Day": pd.Timestamp.now().strftime("%d-%m-%Y"), "BUY/SELL": "SELL", "Quantity": -quantity, "Price": sell_price, "Total": -quantity * sell_price, "P&L": 0}])], ignore_index=True)
    
    # User input for transactions
    st.subheader("New Transaction")
    quantity_input = st.number_input("Enter Quantity", min_value=1, value=1000)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Subscripcion"):
            buy(quantity_input)
            message = st.success(f"Successfully bought {quantity_input} units")
            time.sleep(3)
            message.empty()
            st.rerun()
    with col2:
        if st.button("Reembolso"):
            sell(quantity_input)
            message = st.success(f"Successfully sold {quantity_input} units")
            time.sleep(3)
            message.empty()
            st.rerun()
    
    # Display updated transaction history
    st.subheader("Transaction History")
    st.dataframe(st.session_state.transactions_df)
    
    if st.button("📄 Download Excel"):
        st.session_state.transactions_df.to_excel("transactions.xlsx", index=False)
        st.download_button(label="Download Transactions", data=open("transactions.xlsx", "rb"), file_name="transactions.xlsx", mime="application/vnd.ms-excel")
    
    st.write(f"**FIFO Cost:** {st.session_state.total_cost / max(1, st.session_state.total_quantity):.2f} per unit")
    st.write(f"**P&L Realizado:** {st.session_state.total_pnl:.2f}")
