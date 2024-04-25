import streamlit as st

# Title of the app
st.title("Streamlit State Management Demo")

# Initialize the counter in the session state if it doesn't exist
if 'counter' not in st.session_state:
    st.session_state.counter = 0

# Function to increment the counter
def increment_counter():
    st.session_state.counter += 1

# Function to decrement the counter
def decrement_counter():
    st.session_state.counter -= 1

# Buttons to increment and decrement the counter with instant updates
col1, col2 = st.columns(2)  # Using columns to organize buttons

with col1:
    increment = st.button(':red[Increment Counter]')
    if increment:
        increment_counter()

with col2:
    decrement = st.button(':green[Decrement Counter]')
    if decrement:
        decrement_counter()

# Display the current value of the counter
st.write(f"Current counter value: {st.session_state.counter}")