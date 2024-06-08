from langchain.schema import ChatMessage
from langchain_openai.chat_models import ChatOpenAI
from langchain_openai.llms import OpenAI

import streamlit as st
# from langchain.llms.openai import OpenAI

from openai import AuthenticationError, RateLimitError

from utils.helpers import StreamHandler

st.title('🦜🔗 Quickstart App')

with st.sidebar:
    openai_api_key = st.text_input('OpenAI API Key', type='password')


if "messages" not in st.session_state:
    st.session_state.messages = [
        ChatMessage(
            role="assistant",
            content="Hello! I'm here to help you with your questions."
        )
    ]

for message in st.session_state.messages:
    st.chat_message(message.role).write(message.content)

if prompt := st.chat_input(placeholder='Enter your message:', max_chars=256):
    st.session_state.messages.append(
        ChatMessage(role="user", content=prompt)
    )
    st.chat_message("user").write(prompt)

    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter a valid OpenAI API key beginning with sk-****', icon='⚠')
        st.page_link(page='https://platform.openai.com/account/api-keys', label='Click here to get your OpenAI API Key', icon="🌎")
        st.stop()

    if not openai_api_key:
        st.warning('Please enter your OpenAI API key!', icon='⚠')
        # Return information on how to get the API key from a link
        st.page_link(page='https://platform.openai.com/account/api-keys', label='Click here to get your OpenAI API Key', icon="🌎")
        st.stop()
    
    with st.chat_message("assistant"):
        try:
            stream_handler = StreamHandler(st.empty())
            llm = ChatOpenAI(
                openai_api_key=openai_api_key,
                model="gpt-3.5-turbo",
                temperature=1.0,
                streaming=True,
                callbacks=[stream_handler]
            )
            response = llm.invoke(st.session_state.messages)
            st.session_state.messages.append(
                ChatMessage(
                    role="assistant",
                    content=response.content
                )
            )
            # print("response", response)
        except AuthenticationError:
            st.warning('Invalid OpenAI API key!', icon='⚠')
            st.stop()
        
        except RateLimitError:
            st.warning('OpenAI API rate limit exceeded!', icon='⚠')
            st.stop()
    # if message.role == "assistant":
    #     st.write(message.content)
    # else:
    #     st.write(f'You: {message.content}')
# clear chat history button
if st.button('Clear Chat History'):
    st.session_state.messages = [
        ChatMessage(
            role="assistant",
            content="Hello! I'm here to help you with your questions."
        )
    ]
# def generate_response(input_text):
#     llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
#     st.info(llm(input_text))

# with st.form('my_form'):
#     text = st.text_area('Enter text:', 'What are the three key pieces of advice for learning how to code?')
#     submitted = st.form_submit_button('Submit')
#     if not openai_api_key.startswith('sk-'):
#         st.warning('Please enter your OpenAI API key!', icon='⚠')
#     if submitted and openai_api_key.startswith('sk-'):
#         generate_response(text)
#     else:
#         st.warning('Please enter your OpenAI API key!', icon='⚠')
#         st.info('You can get your API key from the OpenAI dashboard.', icon='ℹ')
#         st.stop()
