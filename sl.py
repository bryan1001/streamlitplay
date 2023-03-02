import streamlit as st
import json
from meals import get_meals

st.title("Meal Plan Generator")

# Get the list of foods to avoid and requirements from the sidebar
st.session_state['avoid'] = st.sidebar.text_input("Enter foods to avoid (e.g. chicken, milk, eggplant, squid):", value=st.session_state.get('avoid',"chicken, milk, eggplant, squid"))
st.session_state['requirements'] = st.sidebar.text_input("Include one of", value=st.session_state.get('requirements',"beef, pork, lamb"))

# Prompt the user to input a list of meals to generate
prompt = f"""You are a master chef, please list 10 dinners that are difficult to prepare.
just the main course.
don't include meals that include any of {st.session_state['avoid']} either in the meal or in a side.
include one of {st.session_state['requirements']} in each meal.

keep the number of total different ingredents to a minimum.
don't include links just a name, a side and no directions in json:\n\n
only respond with:
[{{ "meal": "meal name","description": "description of meal", "ingredients": ["ingredient1"]}}]"""

# Get the list of meals based on the user's input
meals_data = get_meals(prompt)
meals = json.loads(meals_data)

# Create a list to store the selected meals
st.session_state['selected_items'] = st.session_state.get('selected_items',[])


# Loop through the meals and create a checkbox for each one
for meal in meals:
    selected = st.checkbox(meal["meal"])
    st.write(meal["description"])
    if selected and meal not in st.session_state['selected_items']:
        st.session_state['selected_items'].append(meal)
    elif not selected and meal in st.session_state['selected_items']:
        st.session_state['selected_items'].remove(meal)
        

# Create a set to store the ingredients
ingredients_set = set()

# Loop through the selected meals and extract the ingredients
for meal in st.session_state['selected_items']:
    for ingredient in meal["ingredients"]:
        ingredients_set.add(ingredient)

# Convert the set to a list and sort it alphabetically
ingredients_list = sorted(list(ingredients_set))



# Display the selected items
if st.session_state.get('selected_items'):
    st.sidebar.subheader("Selected Items:")
    for meal in st.session_state['selected_items']:
        st.sidebar.write(meal["meal"])

# Display the final shopping list
st.sidebar.subheader("Shopping List")
for ingredient in ingredients_list:
    st.sidebar.write(ingredient)
