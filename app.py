import streamlit as st
from utils import write_message
from agent import generate_response


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
    st.title("Welcome to the Health Claim Graph Chatbot")
    # set explanation 
    with st.expander("About Me"):
        st.write("""
        I am a movie expert! I know about movies, actors, and stuff! You can ask me anything, movie related, and I will try to answer it.
        I can also recommend movies based on actors, directors, and genres. I can even tell you how two actors are connected through movies. Try me out!\n\n
        (but if I made mistakes, please forgive me, I am still learning! 😅)
    """)

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
