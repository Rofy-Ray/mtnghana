import streamlit as st
st.set_page_config(
        page_title="Y'ello Agent🐝",
        page_icon=":bee:",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items=None
    )
import streamlit.components.v1 as components
from config.styles import CSS_STYLES
import base64
import os
from utils.data_processing import load_and_preprocess_data, create_dataset
from utils.agent import generate_response

def process_response(response):
    """Handle different pandasai response types using class name detection"""
    response_type = response.__class__.__name__
    
    try:
        if response_type == 'StringResponse':
            return str(response.value)
            
        elif response_type == 'NumberResponse':
            return f"📊 Result: {response.value:,}"
            
        elif response_type == 'DataFrameResponse':
            return (
                "📋 Data Overview:",
                response.value.head().to_html(classes='styled-table', index=False, border=0, justify='center')
            )
            
        elif response_type == 'ChartResponse':
            if os.path.exists(response.value):
                with open(response.value, "rb") as img_file:
                    base64_img = base64.b64encode(img_file.read()).decode()
                return f'<img src="data:image/png;base64,{base64_img}" style="max-width: 100%;">'
            return "📊 Chart generated but couldn't load image"
            
        elif response_type == 'ErrorResponse':
            return f"❌ Error: {response.value}"
            
        else:
            return str(response)
            
    except Exception as e:
        return f"⚠️ Error processing response: {str(e)}"

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
            {content}
        </div>
    </div>
    """

def main():
    st.logo(image="images/mtnlong.jpg", size="large")
    
    st.markdown(CSS_STYLES, unsafe_allow_html=True)
    
    with st.sidebar:
        st.title("Y'ello Agent:bee:")
        st.markdown("""
                    ### Welcome to Intelligent Data Insights!

                    I'm here to help you understand your data, providing personalized support and expert analysis. My capabilities include:

                    #### Key Features

                    - **Answering Questions:** Get instant answers to your data-related queries.
                    - **Insight Generation:** Uncover hidden patterns and trends in your data.
                    - **Chart Creation:** Visualize your data with informative and engaging charts.

                    #### Advanced Capabilities

                    - **In-Depth Analysis:** Perform complex data analyses to extract meaningful insights.
                    - **Clear Explanations:** Receive concise, easy-to-understand explanations of your data.

                    #### Get Started

                    Feel free to ask me anything about your data! I'm here to help you unlock its full potential.
                    """)
        
    st.title("Hey! I'm Y'ello Agent!:bee:")
    
    initialize_chat_history()
    
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.messages:
            if message.get("type") == "html":
                st.markdown(message["content"], unsafe_allow_html=True)
            else:
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
            raw_response = generate_response(user_input)
            
            if raw_response:
                processed_content = process_response(raw_response)
                
                if isinstance(processed_content, tuple):
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": processed_content[0],
                        "type": "text"
                    })
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": processed_content[1],
                        "type": "html"
                    })
                else:
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": processed_content,
                        "type": "text"
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