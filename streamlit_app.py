# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
 
 
# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruit you want in your custom smoothie!
    """
)
 
name_on_order = st.text_input ('Name on Smoothie')
cnx=st.connection('snowflake')
session=cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
st.dataframe(data=my_dataframe, use_container_width=True)
 
ingredient_list = st.multiselect(
    'choose upto 5 ingredients:',
    my_dataframe,
    max_selections = 5
)
if ingredient_list:
    ingredients_string = ''
    for fruit_chosen in ingredient_list:
        ingredients_string+=fruit_chosen + ' '
    # st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('"""  + ingredients_string +  """','"""  + name_on_order +  """')"""
 
    time_to_insert = st.button('Submit Order')
 
    # st.write(my_insert_stmt)
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your smoothie is ordered ,' + name_on_order + '!', icon = '✅')
