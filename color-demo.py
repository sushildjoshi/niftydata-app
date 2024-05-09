import streamlit as st

# Title of the app
st.title('Webpage Color Design Tool')
st.write('this is demo page')

# Sidebar for color selection
st.sidebar.header("Color Settings")
background_color = st.sidebar.color_picker("Choose a background color", "#FFFFFF")
text_color = st.sidebar.color_picker("Choose a text color", "#000000")
button_color = st.sidebar.color_picker("Choose a button color", "#0084f4")
button_text_color = st.sidebar.color_picker("Choose button text color", "#FFFFFF")

# Using the selected colors in HTML to show a preview
html_template = f"""
<div style='background-color: {background_color}; padding: 10px;'>
    <h1 style='color: {text_color};'>Hello, Streamlit!</h1>
    <button style='background-color: {button_color}; color: {button_text_color}; border: none; padding: 10px 20px;'>
        Click Me!
    </button>
    <p style='color: {text_color};'>This is a simple webpage mockup.</p>
</div>
"""

st.markdown('### Preview of your webpage:')
st.markdown(html_template, unsafe_allow_html=True)