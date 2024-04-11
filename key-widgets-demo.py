import streamlit as st


# Title for your app
st.title('Streamlit Key Widgets Demo')

# Text input
name = st.text_input('Enter your name:')
if name:
    st.write('Hello, ', name, '!')

# Slider
age = st.slider('Select your age:', 0, 100, 25)
st.write("You're ", age, 'years old')

# Button
if st.button('Say hello'):
    st.write('Why hello there')
else:
    st.write('Goodbye')

# Checkbox
if st.checkbox('Show/hide'):
    st.write('Now you see me!')

# Radio buttons
status = st.radio('Select your status:', ('Active', 'Inactive'))
st.write('Status: ', status)

# Selectbox
job = st.selectbox('Your job role:', ('Developer', 'Data Scientist', 'Product Manager'))
st.write('You selected: ', job)

# Multiselect
hobbies = st.multiselect('Select hobbies:', ['Reading', 'Traveling', 'Swimming', 'Cooking'])
st.write('You selected:', hobbies)

# File Uploader
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    st.write("You have uploaded a file.")

# Date Input
import datetime
appointment = st.date_input("Schedule your appointment:", datetime.datetime.now())
st.write("Your appointment is set for:", appointment)



# Color Picker
color = st.color_picker('Pick A Color', '#00f900')
st.write('The selected color is:', color)
