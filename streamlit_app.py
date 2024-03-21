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
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'), col('SEARCH_ON')
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()                                                                      

pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()
 
ingredient_list = st.multiselect(
    'choose upto 5 ingredients:',
    my_dataframe,
    max_selections = 5
)
if ingredient_list:
    ingredients_string = ''
    for fruit_chosen in ingredient_list:
        ingredients_string+=fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        
        st.subheader(fruit_chosen + 'Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_chosen)
        fv_df = st.dataframe(data =fruityvice_response.json(), use_container_width=True)
    # st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('"""  + ingredients_string +  """','"""  + name_on_order +  """')"""
 
    time_to_insert = st.button('Submit Order')
 
    # st.write(my_insert_stmt)
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your smoothie is ordered ,' + name_on_order + '!', icon = '✅')
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# st.text(fruityvice_response).json()
fv_df = st.dataframe(data =fruityvice_response.json(), use_container_width=True)
