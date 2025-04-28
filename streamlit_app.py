# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

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
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# 과일 선택하기
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe.to_pandas()['FRUIT_NAME'].tolist()  # Snowpark 데이터프레임을 리스트로 변환
    , max_selections=5
)

# 주문 제출 버튼
time_to_insert = st.button('Submit Order')

if time_to_insert:
    if ingredients_list and name_on_order:
        # 선택된 과일들을 하나의 문자열로 결합
        ingredients_string = ', '.join(ingredients_list)

        # INSERT 쿼리 생성
        my_insert_stmt = f"""
            INSERT INTO smoothies.public.orders (ingredients, name_on_order)
            VALUES ('{ingredients_string}', '{name_on_order}')
        """
        
        # SQL 실행
        session.sql(my_insert_stmt).collect()

        # 성공 메시지
        st.success(f"Order for {name_on_order} has been successfully placed! 🍓🍌🥭")
    else:
        st.warning("Please enter a name and select at least one ingredient.")

