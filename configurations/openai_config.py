import streamlit as st

def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("app.py", label="Switch accounts")
    st.sidebar.page_link("pages/user.py", label="Your profile")
    if st.session_state.role in ["admin", "super-admin"]:
        st.sidebar.page_link("pages/admin.py", label="Manage users")
        st.sidebar.page_link(
            "pages/super-admin.py",
            label="Manage admin access",
            disabled=st.session_state.role != "super-admin",
        )

def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("app.py", label="Log in")

def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        unauthenticated_menu()
        return
    authenticated_menu()

def openai_config():
    # Set OpenAI model configurations
    with st.sidebar:
        st.subheader('OpenAI Model Configurations')
        # Get OpenAI API Key
        # openai_api_key = st.text_input(
        #     label='OpenAI API Key',
        #     type='password',
        #     value="sk-",
        #     placeholder='Enter your OpenAI API Key',
        #     help='Enter your OpenAI API Key',
        # )

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
    # return map(str, [temperature, max_tokens, top_p, frequency_penalty, presence_penalty, model, stream_response])
    return temperature, max_tokens, top_p, frequency_penalty, presence_penalty, model, stream_response
