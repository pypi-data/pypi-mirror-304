import streamlit as st
from clickable_textbox import clickable_textbox

import time
# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run my_component/example.py`

st.subheader("Component with constant args")

# Create an instance of our component with a constant `name` arg, and
# print its output value.

if 'excerpt_selected' not in st.session_state:
    st.session_state.excerpt_selected = None

def clean_response_for_textbox(input, footnotes):
    for footnote in footnotes:
        input=input.replace(footnote, " </span><span style='color: blue; cursor: pointer;'><u>"+footnote+"</u></span><span>")
    input="<span>"+input+"</span>"
    # \n doesnt work, so replace with <br> for linebreaks
    input=input.replace("\n", "<br>")
    return input

sample_llm_response="""This result comes from Excerpt 1. Excerpt 2 is not mentioned, but maybe you can find what you want in excerpt 3? [1-3] A bi-directional Streamlit Component has two parts: A frontend, which is built out of HTML and any other web tech you like (JavaScript, React, Vue, etc.), and gets rendered in Streamlit apps via an iframe tag. 
A Python API, which Streamlit apps use to instantiate and talk to that frontend [1-47] [2-9] 
To make the process of creating bi-directional Streamlit Components easier, we've created a React template and a TypeScript-only template in the Streamlit Component-template GitHub repo. We also provide some example Components in the same repo.

not sure if a new para works, hopefully it does otherwise we are gonna have to troubleshoot again!"""

with st.spinner('sleeping'):
    time.sleep(1)

@st.fragment
def response_box(response, footnotes):
    excerpt_selected = clickable_textbox(text_to_display=response, height=400, key='foo')
    if (excerpt_selected in footnotes) and (excerpt_selected != st.session_state.excerpt_selected):
        st.session_state.excerpt_selected=excerpt_selected
        st.rerun()

footnotes=["[1-3]", "[2-9]", "[1-47]"]
response=clean_response_for_textbox(sample_llm_response, footnotes)
response_box(response, footnotes)

st.markdown(f"You've selected {st.session_state.excerpt_selected}")

st.markdown("---")