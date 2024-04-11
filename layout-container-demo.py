import streamlit as st

# Title of the app
st.title("Streamlit Layouts & Containers Demo")

# Session state for a counter
if 'counter' not in st.session_state:
    st.session_state.counter = 0

# Using a sidebar for input
with st.sidebar:
    st.write("**This is a sidebar**")
    sidebar_selectbox = st.selectbox("Choose a number:", [1, 2, 3, 4, 5])
    # Increment counter button in sidebar
    if st.button('Increment Counter'):
        st.session_state.counter += 1

# Displaying chosen sidebar option and the counter in the main area
st.write(f"**:green[You selected option {sidebar_selectbox} in the sidebar.]**")
st.write(f"Counter value: {st.session_state.counter}")

# Columns for horizontal layout
st.write("**Columns for horizontal layout**")
col1, col2, col3 = st.columns(3)
with col1:
    st.header("Column 1")
    st.write("This is the first column. You can add any Streamlit widget here.")
    col1_button = st.button("Click me 1")
    if col1_button:
        st.session_state.counter += 1  # Increment counter on button click
        st.write("Button in Column 1 clicked.")

with col2:
    st.header("Column 2")
    st.write("This is the second column. It can have its own widgets.")
    col2_slider = st.slider("Slide me", 0, 100)

with col3:
    st.header("Column 3")
    st.write("This is the third column. Different widgets can be placed here too.")
    col3_checkbox = st.checkbox("Check me")
    if col3_checkbox:
        st.write("Checkbox in Column 3 is checked.")

# Expander for optional information
st.write("**Expander for optional information**")
with st.expander("See explanation"):
    st.write("""
        This is an expander. You can use it to hide optional or additional information
        that is not necessary for the initial view. Click on the expander to show or hide
        the content inside.
    """)

# Containers for organizing content
st.write("**Containers for organizing content**")
with st.container():
    st.write("This is a container.")
    st.write("You can place any Streamlit widget inside a container.")
    st.write("Containers are useful for grouping widgets together.")
    container_slider = st.slider("Slide inside a container", 0, 50)
    st.write(f"Slider in container value: {container_slider}")

# Using tabs for organized content
st.write("**Using tabs for organized content**")
tab1, tab2 = st.tabs(["First Tab", "Second Tab"])
with tab1:
    st.header("This is the first tab")
    st.write("Tabs allow you to organize content in a clean and interactive way.")

with tab2:
    st.header("This is the second tab")
    st.write("You can switch between tabs to view different content sections.")