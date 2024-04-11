import streamlit as st
import time

# Use the st.cache decorator to indicate this function's output should be cached
@st.cache_data
def simulate_expensive_computation(number):
    # Simulate a time-consuming computation with time.sleep()
    time.sleep(5)  # Sleep for 5 seconds to simulate a long computation
    return number * number

# Ask the user for a number
number = st.number_input("Enter a number", value=1, step=1)

# Display a button the user can click to calculate the square of the number
if st.button('Calculate square'):
    # Call the cached function
    result = simulate_expensive_computation(number)
    # Display the result
    st.write(f"The square of {number} is {result}")
else:
    st.write('Click the button to calculate the square of the number.')