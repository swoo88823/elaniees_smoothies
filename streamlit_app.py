# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

# 사용자로부터 이름 입력 받기
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Snowflake 세션 시작
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

# 과일 선택하기
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe.to_pandas()['FRUIT_NAME'].tolist()  # Snowpark 데이터프레임을 리스트로 변환
    , max_selections=5
)

if ingredients_list:
    ingredients_string=''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', furit_chosen,' is ', search_on, '.')

        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)



