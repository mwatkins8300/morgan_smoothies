import streamlit as st
from snowflake.snowpark.functions import col

# App heading
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

# Connect to Snowflake using Streamlit Secrets
connection = st.connection("snowflake")
session = connection.session()

# Customer name
name_on_order = st.text_input("Name on Smoothie:")

if name_on_order:
    st.write(
        "The name on your smoothie will be:",
        name_on_order
    )

# Retrieve the available fruit options
fruit_rows = (
    session.table("smoothies.public.fruit_options")
    .select(col("FRUIT_NAME"))
    .collect()
)

fruit_options = [
    row["FRUIT_NAME"]
    for row in fruit_rows
]

# Ingredient selection
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    options=fruit_options,
    max_selections=5
)

# Submit the order
if ingredients_list:
    ingredients_string = " ".join(ingredients_list)

    if st.button("Submit Order"):
        if not name_on_order.strip():
            st.warning(
                "Please enter a name for your smoothie."
            )
        else:
            insert_statement = """
                INSERT INTO smoothies.public.orders
                    (ingredients, name_on_order)
                VALUES (?, ?)
            """

            try:
                session.sql(
                    insert_statement,
                    params=[
                        ingredients_string,
                        name_on_order.strip()
                    ]
                ).collect()

                st.success(
                    "Your smoothie is ordered!",
                    icon="✅"
                )

            except Exception as error:
                st.error(f"Unable to submit the order: {error}")
