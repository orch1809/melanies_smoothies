# Import python packages
import streamlit as st

from snowflake.snowpark.functions import col
import requests
# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)


name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# option = st.selectbox(
#     'How would you like to be contacted?',
#     ('Email','Home phone','Mobile phone'))

# st.write('You selected',option)



# option = st.selectbox(
#      'What is your favorite fruit?',
#      ('Banana','Strawberries','Peaches'))

# st.write('Your favorite fruit is: ',option)


cnx=st.connection("snowflake")
session= cnx.session()

df= session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=df,use_container_width=True)

ingredients_list= st.multiselect(
    'Choose up to 5 ingredients:'
    ,df
    ,max_selections=5
)
if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    
    ingredients_string=''
    
    for fruit_chosen in ingredients_list:
        ingredients_string+= fruit_chosen + ' '
        st.subheader(fruit_chosen+' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_chosen)
        # st.text(fruityvice_response.json())
        fv_dg=st.dataframe(data=fruityvice_response.json(),use_container_width=True)

    # st.write(ingredients_string)

    my_insert_stmt= """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
            values ('""" + ingredients_string + """','""" + name_on_order+ """')"""

    # st.write(my_insert_stmt)
    # st.stop()
    time_to_insert= st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success('Your Smoothie is ordered!'+name_on_order, icon="✅")
        
