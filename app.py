import streamlit as st
from langchain_community.callbacks import StreamlitCallbackHandler
from agent import agent_executor

from utils import write_message
from PIL import Image

def stick_header():

    # make header sticky.
    st.markdown(
        """
            <div class='fixed-header'/>
            <style>
                div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
                    position: sticky;
                    top: 2.875rem;
                    background-color: white;
                    z-index: 999;
                }
                .fixed-header {
                    /* border-bottom: 1px solid black; */
                }
            </style>
        """,
        unsafe_allow_html=True
    )

with st.container():
    stick_header()

    # Set the title
    st.title("Welcome to the Health Claim Chatbot")
    # set explanation 
    with st.expander("About Me"):
        st.write("""
        I am a medical claim handler expert. Ask me anything about ICD code, disease, illness or health claim fraud patterns. 
        I also have access to claim knowledge based of a sample data(200 claims).\n\n Ask me anything!\n\n
                 
        
        (but if I made mistakes, please forgive me, I am still learning! 😅)
    """)
        image = Image.open('img/claim-sample.png')
        st.image(image)
        image = Image.open('img/schema-visualization.png')
        st.image(image)

# Set up Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, I'm the Claim Graph Chatbot!  Ask me anything about claim 😉"},
    ]

# Display messages in Session State
for message in st.session_state.messages:
    write_message(message['role'], message['content'], save=False)

# Handle any user input
if prompt := st.chat_input("What is up?"):

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
        st.session_state.messages.append({"role":"user", "content": prompt})

    # Generate a response
    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        try:
            response = agent_executor.invoke(
                {"input": prompt}, {"callbacks": [st_callback]}
            )
            output = response.get('output')
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            output="Sorry, there are some errors at the backend. Please try again later."

        st.markdown(output)
        st.session_state.messages.append({"role": "assistant", "content": output})
