import streamlit as st
import openai

@st.cache_data
def get_meals(prompt):
    openai.api_key = st.secrets["openai_api_key"]
    return openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature=0.8, max_tokens=3000,
    messages=[
        {"role": "system", "content": "You are a helpful assistant that only responds in json."},
        {"role": "user", "content": prompt},
    ]
    )['choices'][0]['message']['content']

st.title("Meal Plan Generator")
st.session_state['avoid'] = st.sidebar.text_input("Enter foods to avoid (e.g. chicken, milk, eggplant, squid):", value=st.session_state.get('avoid',"chicken, milk, eggplant, squid"))

st.session_state['requirements'] = st.sidebar.text_input("Include one of", value=st.session_state.get('requirements',"beef, pork, lamb"))

prompt = f"""You are a master chef, please list 10 dinners that kids would like.
just the main course.
don't include meals that include any of {st.session_state['avoid']} either in the meal or in a side.
include one of {st.session_state['requirements']} in each meal.

keep the number of total different ingredents to a minimum.
don't include links just a name, a side and no directions in json:\n\n
only respond with:
[{{ "meal": "meal name","description": "description of meal", "ingredients": ["ingredient1"]}}]"""
st.sidebar.code(prompt)
import json
meals_data = get_meals(prompt)
st.sidebar.write(meals_data)
meals = json.loads(meals_data)
# v = "[" + get_meals(prompt)
# import json

for meal in meals:
    st.subheader(meal["meal"])
    st.write(meal["description"])
    st.write(meal["ingredients"])
    
