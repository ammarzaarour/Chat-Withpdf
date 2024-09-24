import streamlit as st
from backend import run_llm
from streamlit_chat import message
# Sidebar with profile, new chat button, and conversations
with st.sidebar:
    # Logo and version
    st.image("https://w7.pngwing.com/pngs/589/237/png-transparent-orange-and-brown-ai-logo-area-text-symbol-adobe-ai-text-trademark-orange.png", width=100)  # replace with your logo URL or local image
    st.markdown("### Le-AI v0.9.2")
    st.markdown("<span style='color: red;'>New</span>", unsafe_allow_html=True)
    
    # Button for new chat
    if st.button("New Chat"):
        st.session_state['chat_history'] = []  # Clear chat history on new chat
    
    # Sidebar footer for license activation
    st.markdown("---")
    st.write("Le-AI License Activate")
    st.markdown(
        """
        <p>
        <a href="https://github.com" target="_blank">
        <img src="https://img.icons8.com/ios-glyphs/30/000000/github.png"/>
        </a>
        <a href="https://t.me/telegram_channel" target="_blank">
        <img src="https://img.icons8.com/ios-glyphs/30/000000/telegram-app.png"/>
        </a>
        <a href="#" target="_blank">
        <img src="https://img.icons8.com/ios-glyphs/30/000000/language.png"/>
        </a>
        </p>
        """, unsafe_allow_html=True
    )
# Initialize session state if not already present
if (
    "chat_answers_history" not in st.session_state
    and "user_prompt_history" not in st.session_state
    and "chat_history" not in st.session_state
    and "page" not in st.session_state  # Add 'page' to manage navigation
):
    st.session_state["chat_answers_history"] = []
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_history"] = []
# Main content area
st.title("PDF Conversation")

# Custom CSS to style the input box at the bottom and add spacing similar to ChatGPT
st.markdown("""
    <style>
        .chat-container {
            display: flex;
            flex-direction: column;
            height: 80vh;
            justify-content: space-between;
        }
        .chat-history {
            overflow-y: auto;
            padding: 20px;
            background-color: #f7f7f7;
            height: 40vh;
            border: 1px solid #ddd;
            border-radius: 8px;
        }
        .input-container {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
        }
        .stTextInput>div>div {
            width: 100%;
        }
        .stButton>button {
            padding: 8px 20px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
    </style>
""", unsafe_allow_html=True)



# Chat container that includes history and input field
with st.container():
   

    # Input area at the bottom
    st.markdown("<div class='input-container'>", unsafe_allow_html=True)

    prompt = st.text_input("Prompt", placeholder="Enter your message here...") or st.button("Submit")

    if prompt:
        with st.spinner("Generating response..."):
            generated_response = run_llm(
                query=prompt
            )

            st.session_state["user_prompt_history"].append(prompt)
            st.session_state["chat_answers_history"].append(generated_response)
            st.session_state["chat_history"].append(("human", prompt))
            st.session_state["chat_history"].append(("ai", generated_response))

    # Display the chat history with unique keys
    if st.session_state["chat_answers_history"]:
        for i, (generated_response, user_query) in enumerate(
            zip(st.session_state["chat_answers_history"], st.session_state["user_prompt_history"])
        ):
            # Unique key for each user message
            message(user_query, is_user=True, key=f"user_msg_{i}")
            # Unique key for each AI response
            message(generated_response, key=f"ai_msg_{i}")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

