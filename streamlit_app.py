# Import Python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# App heading
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

# Connect to the active Snowflake session
session = get_active_session()

# Customer name
name_on_order = st.text_input("Name on Smoothie:")

if name_on_order:
    st.write("The name on your smoothie will be:", name_on_order)

# Retrieve available fruit options
my_dataframe = (
    session.table("smoothies.public.fruit_options")
    .select(col("FRUIT_NAME"))
)

# Ingredient selection
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)

# Submit the order
if ingredients_list:
    ingredients_string = " ".join(ingredients_list)

    if st.button("Submit Order"):
        if not name_on_order.strip():
            st.warning("Please enter a name for your smoothie.")
        else:
            my_insert_stmt = """
                INSERT INTO smoothies.public.orders
                    (ingredients, name_on_order)
                VALUES (?, ?)
            """

            session.sql(
                my_insert_stmt,
                params=[ingredients_string, name_on_order.strip()]
            ).collect()

            st.success("Your smoothie is ordered!", icon="✅")
