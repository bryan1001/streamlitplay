import openai
import streamlit as st

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
