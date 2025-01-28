import streamlit as st
import streamlit.components.v1 as components
from config.styles import CSS_STYLES
import base64
import os
from utils.data_processing import load_and_preprocess_data, create_sql_db_from_df
from utils.sql_agent import generate_response

def initialize_chat_history():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm Y'ello Agent, your friendly MTN assistant. How can I help you today?"}
        ]
        
def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
    
def create_chat_html(role, content):
    user_icon = get_image_base64("images/user_icon.png")
    bot_icon = get_image_base64("images/bot_icon.png")
    return f"""
    <div class="chat-row {'row-reverse' if role == 'user' else ''}">
        <img class="chat-icon" src="data:image/png;base64,{user_icon if role == 'user' else bot_icon}" width=32 height=32>
        <div class="chat-bubble {role}-bubble">
            &#8203;{content}
        </div>
    </div>
    """

def main():
    st.set_page_config(
        page_title="Y'ello Agent🐝",
        page_icon=":bee:",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items=None
    )
    
    st.logo(image="images/mtnlong.jpg", size="large")
    
    st.markdown(CSS_STYLES, unsafe_allow_html=True)
    
    with st.sidebar:
        st.title("Y'ello Agent:bee:")
        st.markdown("""I'm here to help you with your data queries. 
                I can help answer questions about your data.
                Feel free to ask me anything about your data!""")
        
    st.title("Welcome! I'm Y'ello Agent!:bee:")
    
    initialize_chat_history()
    df = load_and_preprocess_data("data/mymtn.csv")
    create_sql_db_from_df(df)
    
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            st.markdown(
                create_chat_html(message["role"], message["content"]), 
                unsafe_allow_html=True
            )
    
    for _ in range(3):
        st.markdown("")
    
    with st.form("chat-form", clear_on_submit=True):
        cols = st.columns((0.9, 0.1))
        user_input = cols[0].text_input(
            "Chat",
            label_visibility="collapsed",
            key="user_input"
        )
        submitted = cols[1].form_submit_button("Send", type="primary")
        
        if submitted and user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            response = generate_response(user_input)
            if response:
                st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response
                    })
            st.rerun()
    
    components.html("""
    <script>
    const streamlitDoc = window.parent.document;
    const buttons = Array.from(streamlitDoc.querySelectorAll('.stButton > button'));
    const submitButton = buttons.find(el => el.innerText === 'Send');
    
    streamlitDoc.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            submitButton.click();
            e.preventDefault();
        }
    });
    </script>
    """, height=0, width=0)

if __name__ == "__main__":
    main()