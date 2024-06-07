import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark import Session
from streamlit_extras import add_vertical_space as avs
import pandas as pd

#session = get_active_session()
pd.set_option("max_colwidth", None)
num_chunks = 3  # Num-chunks provided as context. Adjust as needed for your use case.

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
      
)

def create_session():
    return Session.builder.configs(st.secrets["snowflake"]).create()

session = create_session()

#def load_data(table_name):
    #st.write(f"Here's some example data from `{table_name}`:")
 #   table = session.table(table_name)
  #  table = table.limit(20)
   # table = table.collect()
    #return table

def load_data(table_name):
    table = session.table(table_name)
    df = table.limit(20).to_pandas()
    return df

table_name = "CC_QUICKSTART_CORTEX_DOCS.DATA.comp_data_bkp"
df = load_data(table_name)

    # Check if data loaded correctly
if isinstance(df, pd.DataFrame):
        # Group by 'prompt' and aggregate the rest of the columns by joining the values as strings
    result_df = df.groupby('PROMPT', as_index=False).agg(lambda x: ' | '.join(x.astype(str)))

        # Save the result to a new CSV file
    result_df.to_csv('merged_data.csv', index=False)

    #st.write("Merged DataFrame:")
    st.dataframe(result_df)
else:
    st.error("Failed to load data into a DataFrame.")

def create_prompt(myquestion, rag,stage,selected_doc):

       # Known prefixes that might need to be removed
    known_prefixes = ['docs/', 'history_docs/']

    # Dynamically remove any known prefix from selected_doc
    for prefix in known_prefixes:
        if selected_doc.startswith(prefix):
            selected_doc = selected_doc[len(prefix):]  # Strip the prefix
            break  # Exit the loop once the prefix is stripped

    stage_table = '@CC_QUICKSTART_CORTEX_DOCS.DATA.history_docs' if stage == 'Marketing Knowledge Base' else '@CC_QUICKSTART_CORTEX_DOCS.DATA.docs'
    if rag:
        cmd = f"""
        WITH results AS (
            SELECT RELATIVE_PATH, VECTOR_COSINE_SIMILARITY(docs_chunks_table.chunk_vec,
                    snowflake.cortex.embed_text_768('e5-base-v2', ?)) AS distance, chunk
            FROM CC_QUICKSTART_CORTEX_DOCS.DATA.docs_chunks_table
            where RELATIVE_PATH = ?
            ORDER BY distance DESC
            LIMIT {num_chunks}
        )
        SELECT chunk, relative_path FROM results
        """
        #where ltrim('{stage_table},RELATIVE_PATH','@') = ?
        
        df_context = session.sql(cmd, params=[myquestion,selected_doc]).to_pandas()
        context_length = len(df_context) - 1
        prompt_context = "".join(df_context.loc[:context_length, 'CHUNK'])
        prompt_context = prompt_context.replace("'", "")
        relative_path = df_context.loc[0, 'RELATIVE_PATH'] if not df_context.empty else "Not Found"
        prompt = f"""
        'You are an expert assistance extracting information from context provided.
        Answer the question based on the context. Be concise and do not hallucinate.
        If you don’t have the information just say so.
        Context: {prompt_context}
        Question:  
        {myquestion}
        Answer: '
        """
        cmd2 = f"SELECT GET_PRESIGNED_URL({stage_table}, '{relative_path}', 360) AS URL_LINK FROM directory({stage_table})"
        df_url_link = session.sql(cmd2).to_pandas()
        url_link = df_url_link.loc[0, 'URL_LINK'] if not df_url_link.empty else "URL not available"
    else:
        prompt = f"'Question:\n{myquestion}\nAnswer: '"
        url_link = "None"
        relative_path = "None"
    return prompt, url_link, relative_path

def complete(myquestion, model_name, rag,stage,selected_doc):
    prompt, url_link, relative_path = create_prompt(myquestion, rag,stage,selected_doc)
    cmd = f"SELECT snowflake.cortex.complete(?,?) AS response"
    df_response = session.sql(cmd, params=[model_name, prompt]).collect()
    return df_response, url_link, relative_path

st.title("Build a Retrieval Augmented Generation (RAG) based LLM assistant using Snowflake Cortex and Streamlit:")
st.write("You can ask questions and decide if you want to use your documents for context or allow the model to create their own response.")
#docs_available = session.sql("ls @docs").collect()
#list_docs = [doc["name"] for doc in docs_available]
#st.dataframe(list_docs)

col11, thumb_col = st.columns([0.45, 1.5])
with col11:
    model = st.selectbox('Choose LLM model:', (
         'mistral-7b', 'mistral-large', 'mixtral-8x7b', 'gemma-7b'))



avs.add_vertical_space(4)



tab1, tab2 = st.tabs(["Unstructured", "Structured"])
with tab1:
    col22, thumb_col = st.columns([0.45, 1.5])
    with col22:
        stage = st.selectbox('Business Function(Stage)',(
                                           'Marketing Knowledge Base',
                                           'Sales Knowledge Base',
                                           'HR Knowledge Base'
                                    ))
        stage_table = '@CC_QUICKSTART_CORTEX_DOCS.DATA.history_docs' if stage == 'Marketing Knowledge Base' else '@CC_QUICKSTART_CORTEX_DOCS.DATA.docs'
        docs_available = session.sql(f"ls {stage_table}").collect()
        list_docs = [doc["name"] for doc in docs_available]

    col33, thumb_col = st.columns([0.45, 1.5])
    with col33:
        selected_doc = st.selectbox('Context(Dataset)', list_docs)

    avs.add_vertical_space(4)
   
tab1, tab2 = st.tabs(["Interactive", "Comparison"])
with tab1:
    prompt_options = ["", "what is calculated columns", "Is there any special lubricant to be used with the premium bike?", "What is the warranty for the premium bike?"]
    col44, thumb_col = st.columns([1, 1.5])
    with col44:
        prompt = st.selectbox('Choose prompt', prompt_options, index=0, format_func=lambda x: 'Select prompt...' if x == '' else x)
    
    col55, thumb_col = st.columns([1, 1.5])
    with col55:
        question = st.text_input("Or Enter Your Own Prompt")
       
if st.button(':red[Submit]'):
    actual_question = prompt if prompt else question
    if actual_question:
        st.session_state['actual_question'] = actual_question
        st.session_state['stage'] = stage
        st.session_state['selected_doc'] = selected_doc
        st.session_state['submitted'] = True

if 'submitted' in st.session_state:
    col1, thumb_col, col2 = st.columns([3.5, 1, 3.5])
    with col1:
        st.header("Vanilla Response from LLM")
        response, _, _ = complete(st.session_state['actual_question'], model, 0,st.session_state['stage'], st.session_state['selected_doc'])
        st.markdown(response[0].RESPONSE)
    with thumb_col:
        st.header("Rate")  # Header for the thumbs-up column
        if st.button('👍'):
            if 'clicked' not in st.session_state:
                st.session_state['clicked'] = True
            st.snow()  # Simple interaction: balloons appear on click
    with col2:
        st.header("RAG powered Response from LLM")
        response, url_link, relative_path = complete(st.session_state['actual_question'], model, 1,st.session_state['stage'], st.session_state['selected_doc'])
        st.markdown(response[0].RESPONSE)
        if url_link != "None":
            display_url = f"Link to [{relative_path}]({url_link}) that may be useful"
            st.markdown(display_url)

with tab2:

    # data = {
    # "Prompt": ["what is calculated columns"] + [""] * 1 ,
    # "Model Name": ["mistral-7b", "mistral-large"],
    # "Result via LLM": ["In the context of data analysis and data modeling, a calculated column is a column in a data table that is not populated with data directly from a data source but instead is generated by applying a calculation or formula to one or more existing columns in the table.\n For example, you might have a table of sales data with columns for Sales Amount and Number of Units Sold.\n You could create a calculated column called Total Sales that multiplies the Sales Amount and Number of Units Sold columns to get the total revenue for each row","Calculated columns are columns in a database or spreadsheet that are not directly input by the user, but" ] ,
    # "Result via RAG": ["The passage does not provide information on what is calculated in columns. However, it does mention that the discussion in the book is presented as a narrative, and that the physical setting of India is introduced in the first chapter. The physical setting is described as a landform, and the chapter will discuss India's geography and how it has influenced the development of communities and states throughout history.","Calculated columns are new, formula-based columns that can be added to tables in a data model"] 
# }

    #df = pd.DataFrame(data)
    #df = load_data(table_name)
    # Load data into DataFrame

        
    
    st.write("This table shows the responses from different models to the same prompt.")
    st.dataframe(result_df)
    # def highlight_empty(s):
        # """ Highlight empty strings in a Series yellow. """
        # return ['background-color: lightgrey' if v == "" else 'background-color: white' for v in s]

    #st.dataframe(df)
    # Group by 'prompt' and aggregate the rest of the columns by joining the values as strings
    #result_df = df.groupby('prompt', as_index=False).agg(lambda x: ' | '.join(x.astype(str)))

# Save the result to a new CSV file
    #result_df.to_csv('merged_data.csv', index=False)

    #print("Merged DataFrame:")
#    print(result_df)
     