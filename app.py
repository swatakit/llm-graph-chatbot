import streamlit as st
from langchain_community.callbacks import StreamlitCallbackHandler
from agent import agent_executor

from utils import write_message
from PIL import Image

st.set_page_config(
    page_title="Health Claim Robot",
    page_icon="🤖",
)

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
        st.markdown("""
        I am a medical claim handler expert. Ask me anything about ICD code, disease, illness or health claim fraud patterns. 
        I also have access to claim knowledge based of a sample data(200 claims).\n\n Ask me anything!\n\n
                 
        (but if I made mistakes, please forgive me, I am still learning! 😅)

    """)
        image = Image.open('img/claim-sample.png')
        st.image(image)
        image = Image.open('img/schema-visualization.png')
        st.image(image)
        st.markdown("""
        **Example of questions you can ask me:**
        - Hello, who are you?
        - Who is Elon Musk?
        - Can you give me a poem about illness?
        - can you tell me a bit about acute broncithis, symptom, prescribe medicine, general treatment for a 30 years old?
        - does it usually require lung xray or lab test
        - what is the ICD 10 Code for acute bronchitis?
        - What is the general pattern in fraud health claim?
        - can you search for number 3 
        - can you search for claim that mentioned a healthcare provider submits a claim for a more expensive service or item than was actually provided or necessary, inflating the bill sent to the insurance company.
        - Find a customer "Devon Q. White" and contact information
        - Find phone numbers shared by 2 or more customers
        - Find emails shared by 2 or more customers
        - How many claims do we have in the database and how many claim that has been identified as fraud
        - What are the top claim count by disease?
        - Which agent has the most fraud claim?
        - Find all customers who has association with agent "Avery H. Jackson"
        - Find all hospital that provided medical care to the above customers
        - Can you list the name of the customers who filed many claims in many hospital

    """)        

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
