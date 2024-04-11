import streamlit as st
import pandas as pd

# Load or initialize your Excel file
EXCEL_FILE = 'library_data.xlsx'

try:
    df = pd.read_excel(EXCEL_FILE)
except FileNotFoundError:
    df = pd.DataFrame(columns=['Book Name', 'Code', 'Author', 'Status', 'Issued By', 'Card ID'])
    df.to_excel(EXCEL_FILE, index=False)

def add_book(book_name, code, author):
    new_book = pd.DataFrame({'Book Name': [book_name], 'Code': [code], 'Author': [author], 'Status': ['Available'], 'Issued By': [''], 'Card ID': ['']})
    global df
    df = pd.concat([df, new_book], ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)

def update_status(code, status, issued_by='', card_id=''):
    global df
    book_index = df.index[df['Code'] == code].tolist()[0]
    df.at[book_index, 'Status'] = status
    df.at[book_index, 'Issued By'] = issued_by
    df.at[book_index, 'Card ID'] = card_id
    df.to_excel(EXCEL_FILE, index=False)

def delete_book(code):
    global df
    df = df[df['Code'] != code]
    df.to_excel(EXCEL_FILE, index=False)

# Streamlit UI
st.title('Library Management System')

st.header('Add New Book')
with st.expander("**:red[Please fill this form]**"):
    with st.form("Add book form", clear_on_submit=True):
        book_name = st.text_input('Book Name')
        code = st.text_input('Code')
        author = st.text_input('Author')
        submitted = st.form_submit_button("Add Book")
    if submitted:
        add_book(book_name, code, author)
        st.success(f'Book "{book_name}" added successfully!')

st.header('Update Book Status')
with st.expander("**:red[Please fill this form]**"):
    with st.form("Update book form", clear_on_submit=True):
        code = st.text_input('Book Code for Status Update')
        status = st.selectbox('Status', ['Issued', 'Returned'])
        issued_by = st.text_input('Issued By (for Issued status only)')
        card_id = st.text_input('Card ID (for Issued status only)')
        update_submitted = st.form_submit_button("Update Status")
    if update_submitted:
        update_status(code, status, issued_by, card_id)
        st.success(f'Status of book with code "{code}" updated to "{status}"!')

st.header('Delete Book')
with st.form("Delete book form", clear_on_submit=True):
    delete_code = st.text_input('Enter Code of Book to Delete')
    delete_submitted = st.form_submit_button("Delete Book")
    if delete_submitted:
        delete_book(delete_code)
        st.success(f'Book with code "{delete_code}" deleted successfully!')

st.header('Library Catalogue')
st.dataframe(df)