import streamlit as st
import pandas as pd

cols = st.columns(2)
# Define the schema for the t_shirts table
t_shirts_schema = {
    "Column Name": [
        "t_shirt_id",
        "brand",
        "color",
        "size",
        "price",
        "stock_quantity"
    ],
    "Data Type": [
        "INTEGER (AUTO_INCREMENT)",
        "ENUM('Van Huesen','Levi','Nike','Adidas')",
        "ENUM('Red','Blue','Black','White')",
        "ENUM('XS','S','M','L','XL')",
        "INTEGER",
        "INTEGER"
    ],
    "Nullable": [
        "No",
        "No",
        "No",
        "No",
        "Yes",
        "No"
    ],
    "Default": ["None","None","None","None","None","None"
    ],
    
    "Constraints / Extra Info": [
        "Primary Key",
        "None",
        "None",
        "None",
        "Check Constraint: price between 10 and 50",
        "None"
    ]
}

# Define the schema for the discounts table
discounts_schema = {
    "Column Name": [
        "discount_id",
        "t_shirt_id",
        "pct_discount"
    ],
    "Data Type": [
        "INTEGER (AUTO_INCREMENT)",
        "INTEGER",
        "DECIMAL(5,2)"
    ],
    "Nullable": [
        "No",
        "No",
        "Yes"
    ],
    "Default": [
        "None",
        "None",
        "None"
    ],
    "Constraints / Extra Info": [
        "Primary Key",
        "Foreign Key: References t_shirts(t_shirt_id)",
        "Check Constraint: pct_discount between 0 and 100"
    ]
}

# Convert dictionaries into DataFrames
df_t_shirts = pd.DataFrame(t_shirts_schema)
df_discounts = pd.DataFrame(discounts_schema)

# Display the table schemas in Streamlit
st.title("Database Schema Overview")

st.header("t_shirts Table Schema")
cols[0].table(df_t_shirts)

st.header("discounts Table Schema")
st.table(df_discounts)
