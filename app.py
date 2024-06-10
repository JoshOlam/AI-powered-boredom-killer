from langchain.schema import ChatMessage
from langchain_openai.chat_models import ChatOpenAI
from langchain_openai.llms import OpenAI

import streamlit as st
# from langchain.llms.openai import OpenAI

from openai import AuthenticationError, RateLimitError

from utils.helpers import StreamHandler

# Set the page configurations


# Set the page icon and title
st.set_page_config(
    page_title="AI-Powered-Boredome-Killer with OpenAI and Langchain",
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
st.title('🦜🔗 AI-Powered-Boredome-Killer')
st.subheader('Powered by OpenAI and Langchain')
st.subheader('Served to You by Streamlit')

# with st.sidebar:

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

    temperature = st.slider(
        label='Temperature',
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        help="Controls randomness: Lowering results in less random completions. \
As the temperature approaches zero,the model will become deterministic and repetitive."
    )

    max_tokens = st.number_input(
        label='Max Tokens',
        min_value=1,
        max_value=4095,
        value=100,
        step=10,
        help="The maximum number of tokens to generate shared between the prompt and \
completion. The exact limit varies by model. (One token is roughly 4 characters for \
standard English text)"
    )

    top_p = st.slider(
        label='Top P',
        min_value=0.0,
        max_value=1.0,
        value=1.0,
        help="Controls diversity via nucleus sampling: 0.5 means half of all \
likelihood-weighted options are considered."
    )

    frequency_penalty = st.slider(
        label='Frequency Penalty',
        min_value=0.0,
        max_value=1.0,
        value=0.0,
        help="How much to penalize new tokens based on their existing frequency in \
the text so far. Decreases the model's likelihood to repeat the same line verbatim."
    )

    presence_penalty = st.slider(
        label='Presence Penalty',
        min_value=0.0,
        max_value=1.0,
        value=0.0,
        help="How much to penalize new tokens based on whether they appear in the text \
so far. Increases the model's likelihood to talk about new topics."
    )

    model = st.selectbox(
        label='Model',
        options=[
            'gpt-3.5-turbo',
            'gpt-4-turbo',
            'gpt-4o',
        ],
        index=0,
        help="The model to use for the completion."
    )
    stream_response = st.checkbox(
        label='Stream Response',
        value=True,
        help="Stream the response as it is generated."
    )

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

# clear chat history button
if st.button('Clear Chat History'):
    st.session_state.messages = [
        ChatMessage(
            role="assistant",
            content="Hello! I'm here to help you with your questions."
        )
    ]
    st.rerun()
