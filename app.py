
import os
import streamlit as st

from langchain_ollama import ChatOllama
from langchain_classic.memory import (
    ConversationBufferMemory,
    ConversationSummaryMemory,
    ConversationBufferWindowMemory
)
from langchain_core.prompts import ChatPromptTemplate



st.set_page_config(
    page_title="Cortex - AI Chatbot",
    page_icon="💬",
    layout="wide"
)

st.markdown("""
<style>

/* Main background */
.stApp {
    background: linear-gradient(135deg, #101827, #172554);
    color: white;
}

/* Main title */
.main-title {
    font-size: 38px;
    font-weight: 800;
    color: #60A5FA;
    text-align: center;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #CBD5E1;
    font-size: 16px;
    margin-bottom: 25px;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    border-radius: 14px;
    padding: 12px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

/* Chat input background */
[data-testid="stChatInput"] {
    background-color: #FFFFFF !important;
    border-radius: 12px !important;
}

/* Text while typing */
[data-testid="stChatInput"] textarea {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    caret-color: #000000 !important;
    background-color: #FFFFFF !important;
}

/* Placeholder text */
[data-testid="stChatInput"] textarea::placeholder {
    color: #666666 !important;
    -webkit-text-fill-color: #666666 !important;
    opacity: 1 !important;
}

/* Focus border */
[data-testid="stChatInput"]:focus-within {
    border-color: #60A5FA !important;
}

</style>
""", unsafe_allow_html=True)


if "chats" not in st.session_state:
    st.session_state.chats = {
        "Buffer Memory": [],
        "Summary Memory": [],
        "Window Memory": []
    }

if "memories" not in st.session_state:
    st.session_state.memories = {}


def get_ollama_url():

    url = os.getenv("OLLAMA_BASE_URL")

    if not url:
        try:
            url = st.secrets.get(
                "OLLAMA_BASE_URL",
                "http://localhost:11434"
            )
        except Exception:
            url = "http://localhost:11434"

    return url


@st.cache_resource
def load_llm(model_name, base_url):

    return ChatOllama(
        model=model_name,
        base_url=base_url,
        temperature=0.7
    )


def create_memory(memory_type, llm):

    if memory_type == "Buffer Memory":

        return ConversationBufferMemory(
            memory_key="history",
            input_key="input",
            output_key="output",
            return_messages=False
        )

    elif memory_type == "Summary Memory":

        return ConversationSummaryMemory(
            llm=llm,
            memory_key="history",
            input_key="input",
            output_key="output",
            return_messages=False
        )

    elif memory_type == "Window Memory":

        return ConversationBufferWindowMemory(
            k=3,
            memory_key="history",
            input_key="input",
            output_key="output",
            return_messages=False
        )


def get_memory(memory_type, llm):

    if memory_type not in st.session_state.memories:

        st.session_state.memories[memory_type] = (
            create_memory(memory_type, llm)
        )

    return st.session_state.memories[memory_type]


def generate_response(user_input, llm, memory):

    # Retrieve previous conversation
    memory_data = memory.load_memory_variables({})

    history = memory_data.get("history", "")

    # Create prompt
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            You are Cortex, an intelligent and friendly AI assistant.

            Instructions:
            - Give clear and useful answers.
            - Remember relevant information from conversation history.
            - Answer in simple English.
            - Avoid repeating unnecessary information.
            """
        ),
        (
            "human",
            """
            Previous Conversation:
            {history}

            Current Question:
            {input}
            """
        )
    ])

    # Generate response using Ollama
    chain = prompt | llm

    response = chain.invoke({
        "history": history,
        "input": user_input
    })

    answer = response.content

    # Save conversation into selected memory
    memory.save_context(
        {"input": user_input},
        {"output": answer}
    )

    return answer


st.sidebar.title("Cortex Settings")

model_name = st.sidebar.selectbox(
    "Select Local LLM",
    ["llama3.2", "llama3.1", "mistral"]
)

memory_type = st.sidebar.selectbox(
    "Select Memory Type",
    [
        "Buffer Memory",
        "Summary Memory",
        "Window Memory"
    ]
)

st.sidebar.markdown("---")

st.sidebar.subheader("Memory Information")

memory_descriptions = {
    "Buffer Memory":
        "Stores the complete conversation history.",

    "Summary Memory":
        "Creates a running summary of previous conversations.",

    "Window Memory":
        "Stores only the latest 3 conversation exchanges."
}

st.sidebar.info(memory_descriptions[memory_type])

st.sidebar.markdown("---")

if st.sidebar.button("Clear Current Chat", use_container_width=True):

    st.session_state.chats[memory_type] = []

    if memory_type in st.session_state.memories:
        st.session_state.memories[memory_type].clear()

    st.rerun()

if st.sidebar.button("Clear All Memories", use_container_width=True):

    st.session_state.chats = {
        "Buffer Memory": [],
        "Summary Memory": [],
        "Window Memory": []
    }

    st.session_state.memories = {}

    st.rerun()


st.markdown(
    '<div class="main-title">CORTEX AI CHATBOT</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Local LLM powered by Ollama and LangChain Memory'
    '</div>',
    unsafe_allow_html=True
)

st.caption(f"Active memory: {memory_type} | Model: {model_name}")


try:

    llm = load_llm(model_name, get_ollama_url())

    memory = get_memory(memory_type, llm)

except Exception as error:

    st.error(f"Model initialization failed: {error}")
    st.stop()


for message in st.session_state.chats[memory_type]:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ==========================================
# CHAT INPUT
# ==========================================

user_input = st.chat_input("Ask Cortex anything...")


if user_input:

    # Display user message
    st.session_state.chats[memory_type].append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate AI response
    with st.chat_message("assistant"):

        with st.spinner("Cortex is thinking..."):

            try:

                answer = generate_response(
                    user_input,
                    llm,
                    memory
                )

                st.markdown(answer)

                st.session_state.chats[memory_type].append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as error:

                st.error(
                    f"Unable to generate response: {error}"
                )

                st.info(
                    "Check whether Ollama is running "
                    "and the selected model is installed."
                )


with st.expander("View Memory Contents"):

    memory_data = memory.load_memory_variables({})

    st.write("Selected Memory:", memory_type)

    st.write(memory_data.get("history", "No memory available yet."))

