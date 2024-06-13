from langchain.schema import ChatMessage
from langchain_openai.chat_models import ChatOpenAI

from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import HumanMessage, SystemMessage

from langchain_core.output_parsers import StrOutputParser

import streamlit as st
# from langchain.llms.openai import OpenAI

from openai import AuthenticationError, RateLimitError

from utils.helpers import StreamHandler
# from menu import menu
from configurations.openai_config import openai_config


# Set the page icon and title
st.set_page_config(
    page_title="AI-Powered-Boredom-Killer with OpenAI and Langchain",
    page_icon="🌐",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'mailto:jolalemi@gmail.com',
        'Report a bug': 'mailto:jolalemi@gmail.com',
        'About': "This is a header. This is an *extremely* cool app!"
    }
)

# 
st.title('🦜🔗 AI-Powered-Boredom-Killer')
st.subheader('Powered by OpenAI and Langchain')
st.subheader('Served to You by Streamlit')

# Set OpenAI model configurations
with st.sidebar:
    st.subheader('OpenAI Model Configurations')
    # Get OpenAI API Key
    openai_api_key = st.text_input(
        label='OpenAI API Key',
        type='password',
        value="sk-",
        placeholder='Enter your OpenAI API Key',
        help='Enter your OpenAI API Key',
    )

temperature, max_tokens, top_p, frequency_penalty, presence_penalty, \
    model, stream_response = openai_config()

if "messages" not in st.session_state:
    st.session_state.messages = [
        ChatMessage(
            role="assistant",
            content="Hello 👋! I'm here to help you with your questions."
        )
    ]

for message in st.session_state.messages:
    st.chat_message(message.role).write(message.content)

# Build the prompt
system_messages = """You are an AI assistant powered by OpenAI and \
Langchain, who is extremely sarcastic and ironical, and helps users kill \
boredom with sarcasm, jokes, ironies, and meaningful games. Now, start \
chatting by suggesting what you want the user to do."""
system_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=system_messages
        ),
        # HumanMessagePromptTemplate.from_template(
        #     template="Enter your message:"
        # ),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
    ]
)

# Output parser
output_parser = StrOutputParser()

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
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                streaming=stream_response,
                callbacks=[stream_handler],
                model_kwargs={
                    "presence_penalty": presence_penalty,
                    "frequency_penalty": frequency_penalty,
                    "top_p": top_p,
                }
            )
            llm_chain = system_prompt | llm #| output_parser
            response = llm_chain.invoke(
                {"chat_history": st.session_state.messages},
            )
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

# clear chat history button
if st.button('Clear Chat History'):
    st.session_state.messages = [
        ChatMessage(
            role="assistant",
            content="Hello 👋! I'm here to help you with your questions."
        )
    ]
    st.rerun()
