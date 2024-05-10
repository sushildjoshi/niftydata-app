import streamlit as st
from snowflake.snowpark.context import get_active_session
from streamlit_extras import add_vertical_space as avs
import pandas as pd

session = get_active_session()
pd.set_option("max_colwidth", None)
num_chunks = 3  # Num-chunks provided as context. Adjust as needed for your use case.

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
      
)

def create_prompt(myquestion, rag,stage):
    # Determine the stage-specific table
    #table_map = {
     #   'Marketing Knowledge Base': '@history_docs',
      #  'Sales Knowledge Base': '@docs',
       # 'HR Knowledge Base': '@docs'  # Assuming HR uses the same as Sales for this example
    #}
    #stage_table = table_map.get(stage, '@docs')  # Default to @docs if no specific stage match
    #stage_table = table_map[stage]
    stage_table = '@history_docs' if stage == 'Marketing Knowledge Base' else '@docs'
    if rag:
        cmd = f"""
        WITH results AS (
            SELECT RELATIVE_PATH, VECTOR_COSINE_SIMILARITY(docs_chunks_table.chunk_vec,
                    snowflake.cortex.embed_text_768('e5-base-v2', ?)) AS distance, chunk
            FROM docs_chunks_table
            ORDER BY distance DESC
            LIMIT ?
        )
        SELECT chunk, relative_path FROM results
        """
        df_context = session.sql(cmd, params=[myquestion, num_chunks]).to_pandas()
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

def complete(myquestion, model_name, rag,stage):
    prompt, url_link, relative_path = create_prompt(myquestion, rag,stage)
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
        stage_table = '@history_docs' if stage == 'Marketing Knowledge Base' else '@docs'
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
        st.session_state['submitted'] = True

if 'submitted' in st.session_state:
    col1, thumb_col, col2 = st.columns([3.5, 1, 3.5])
    with col1:
        st.header("Vanilla Response from LLM")
        response, _, _ = complete(st.session_state['actual_question'], model, 0,stage)
        st.markdown(response[0].RESPONSE)
    with thumb_col:
        st.header("Rate")  # Header for the thumbs-up column
        if st.button('👍'):
            if 'clicked' not in st.session_state:
                st.session_state['clicked'] = True
            st.snow()  # Simple interaction: balloons appear on click
    with col2:
        st.header("RAG powered Response from LLM")
        response, url_link, relative_path = complete(st.session_state['actual_question'], model, 1,stage)
        st.markdown(response[0].RESPONSE)
        if url_link != "None":
            display_url = f"Link to [{relative_path}]({url_link}) that may be useful"
            st.markdown(display_url)
