import streamlit as st
from utils import write_message
from agent import generate_response
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


# Submit handler
def handle_submit(message):
    """
    Submit handler:

    You will modify this method to talk with an LLM and provide
    context using data from Neo4j.
    """

    # Handle the response
    with st.spinner('Thinking...'):
        response = generate_response(message)
        write_message('assistant', response)
# end::submit[]


# Display messages in Session State
for message in st.session_state.messages:
    write_message(message['role'], message['content'], save=False)

# Handle any user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    write_message('user', prompt)

    # Generate a response
    handle_submit(prompt)
