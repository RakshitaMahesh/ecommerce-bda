
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="E-Commerce Transaction Analysis",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 E-Commerce Transaction Analysis")
st.caption("Big Data Analytics Mini Project | Interactive Transaction Dashboard")

# Initialize transaction data
if "transactions" not in st.session_state:
    st.session_state.transactions = pd.DataFrame([
        {"Transaction ID": "T001", "Amount": 2500, "Payment": "UPI", "Status": "Success", "Category": "Electronics"},
        {"Transaction ID": "T002", "Amount": 1200, "Payment": "Card", "Status": "Success", "Category": "Clothing"},
        {"Transaction ID": "T003", "Amount": 850, "Payment": "Cash", "Status": "Failed", "Category": "Grocery"},
        {"Transaction ID": "T004", "Amount": 5000, "Payment": "UPI", "Status": "Success", "Category": "Electronics"},
        {"Transaction ID": "T005", "Amount": 750, "Payment": "Card", "Status": "Success", "Category": "Grocery"},
    ])

# Sidebar: add transaction
st.sidebar.header("➕ Add Transaction")

with st.sidebar.form("transaction_form", clear_on_submit=True):
    transaction_id = st.text_input("Transaction ID")
    amount = st.number_input("Amount (₹)", min_value=0.0, step=100.0)
    payment = st.selectbox("Payment Method", ["UPI", "Card", "Cash"])
    status = st.selectbox("Transaction Status", ["Success", "Failed"])
    category = st.selectbox(
        "Category",
        ["Electronics", "Clothing", "Grocery", "Home", "Books", "Other"]
    )

    submitted = st.form_submit_button("Add Transaction")

    if submitted:
        if not transaction_id.strip():
            st.sidebar.error("Please enter a transaction ID.")
        elif transaction_id.strip() in st.session_state.transactions["Transaction ID"].values:
            st.sidebar.error("Transaction ID already exists.")
        else:
            new_row = pd.DataFrame([{
                "Transaction ID": transaction_id.strip(),
                "Amount": amount,
                "Payment": payment,
                "Status": status,
                "Category": category
            }])
            st.session_state.transactions = pd.concat(
                [st.session_state.transactions, new_row],
                ignore_index=True
            )
            st.sidebar.success("Transaction added!")
            st.rerun()

# Dataset
df = st.session_state.transactions.copy()

# Dashboard metrics
total_transactions = len(df)
total_amount = df["Amount"].sum()
successful_sales = df.loc[df["Status"] == "Success", "Amount"].sum()
failed_transactions = int((df["Status"] == "Failed").sum())

st.subheader("📊 Transaction Overview")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Transactions", total_transactions)
c2.metric("Total Transaction Value", f"₹{total_amount:,.2f}")
c3.metric("Successful Sales", f"₹{successful_sales:,.2f}")
c4.metric("Failed Transactions", failed_transactions)

st.divider()

# Charts
left, right = st.columns(2)

with left:
    st.subheader("Sales by Category")
    category_sales = (
        df[df["Status"] == "Success"]
        .groupby("Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )
    if not category_sales.empty:
        st.bar_chart(category_sales)
    else:
        st.info("No successful sales to display.")

with right:
    st.subheader("Transactions by Payment Method")
    payment_counts = (
        df[df["Status"] == "Success"]
        .groupby("Payment")["Transaction ID"]
        .count()
    )
    if not payment_counts.empty:
        st.bar_chart(payment_counts)
    else:
        st.info("No successful transactions to display.")

# Upload CSV
st.divider()
st.subheader("📁 Upload Transaction Dataset")
st.write(
    "Upload a CSV containing these columns: "
    "Transaction ID, Amount, Payment, Status, Category."
)

uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    uploaded_df = pd.read_csv(uploaded_file)
    required_columns = [
        "Transaction ID", "Amount", "Payment", "Status", "Category"
    ]

    if all(column in uploaded_df.columns for column in required_columns):
        st.write("Uploaded dataset preview")
        st.dataframe(uploaded_df, use_container_width=True)

        if st.button("Analyze Uploaded Dataset"):
            st.session_state.uploaded_analysis = uploaded_df
            st.success("Dataset analyzed successfully!")

    else:
        st.error(
            "CSV columns do not match the required format. "
            "Please check the column names."
        )

if "uploaded_analysis" in st.session_state:
    analysis_df = st.session_state.uploaded_analysis.copy()

    st.subheader("Uploaded Dataset Results")
    a1, a2, a3 = st.columns(3)
    a1.metric("Uploaded Transactions", len(analysis_df))
    a2.metric(
        "Uploaded Transaction Value",
        f"₹{pd.to_numeric(analysis_df['Amount'], errors='coerce').fillna(0).sum():,.2f}"
    )

    successful_amounts = pd.to_numeric(
        analysis_df.loc[
            analysis_df["Status"].astype(str).str.lower() == "success",
            "Amount"
        ],
        errors="coerce"
    ).fillna(0)

    a3.metric("Uploaded Successful Sales", f"₹{successful_amounts.sum():,.2f}")

# Full transaction table
st.divider()
st.subheader("📋 Transaction Records")
st.dataframe(df, use_container_width=True, hide_index=True)

csv_data = df.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Download Transactions as CSV",
    data=csv_data,
    file_name="ecommerce_transactions.csv",
    mime="text/csv"
)

if st.button("Reset to Sample Data"):
    del st.session_state["transactions"]
    st.rerun()

st.caption(
    "Note: This version calculates analytics in Python using pandas. "
    "Hadoop MapReduce integration is a separate step."
)
