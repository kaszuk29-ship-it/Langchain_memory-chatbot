# Cortex AI Chatbot

An AI-powered chatbot built using **Ollama, LangChain, and Streamlit**. This project demonstrates how Large Language Models (LLMs) can maintain conversational context using different memory mechanisms.

## Live Demo

https://langchainmemory-chatbot-qvz3sgvoejaed7skhjvwaa.streamlit.app/

## Project Overview

Cortex AI Chatbot is a simple interactive chatbot that uses an LLM to generate responses and maintain conversation history.

It demonstrates three LangChain memory techniques:

- **Conversation Buffer Memory:** Stores the complete conversation history.
- **Conversation Summary Memory:** Summarizes previous conversations to maintain important context.
- **Conversation Buffer Window Memory:** Maintains only a limited number of recent conversation exchanges.

The application provides an interactive Streamlit interface where users can chat with the model and explore different memory strategies.

## Features

- Interactive chatbot interface.
- Local LLM integration using Ollama.
- LangChain integration for conversation management.
- Three different conversation memory mechanisms.
- Maintains conversational context across messages.
- Streamlit-based web application.
- Simple and user-friendly interface.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Ollama | Runs the Large Language Model |
| LangChain | LLM integration and memory management |
| Streamlit | Web application interface |
| LangChain Classic | Conversation memory components |

## Memory Mechanisms

### 1. Conversation Buffer Memory
Stores the entire conversation history and uses it as context for generating future responses.

### 2. Conversation Summary Memory
Creates summaries of previous conversations to retain important information while reducing the amount of conversation history passed to the model.

### 3. Conversation Buffer Window Memory
Stores only the most recent K conversation exchanges, helping the chatbot focus on recent interactions.

## Project Structure

```text
Cortex-AI-Chatbot/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```
## Screenshots

<img width="637" height="331" alt="image" src="https://github.com/user-attachments/assets/403f49de-9553-4ead-86c1-59dd396e667c" />

<img width="633" height="332" alt="image" src="https://github.com/user-attachments/assets/b0281187-5169-479c-84a9-fd398fadc8cb" />

## Installation and Setup

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### Step 2: Navigate to the Project Folder

```bash
cd Cortex-AI-Chatbot
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Set Up Ollama

Install Ollama and download the model used by the application.

For example:

```bash
ollama pull llama3.2
```

Make sure Ollama is running before starting the application.

### Step 6: Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

## Deployment

The application is designed to run through Streamlit and can be deployed using Streamlit Community Cloud.

**Note:** A deployed application needs access to a reachable model endpoint. A local Ollama installation on your computer is not automatically available to Streamlit Community Cloud.

## Learning Outcomes

- Understanding Large Language Models.
- Integrating Ollama with LangChain.
- Implementing different conversation memory techniques.
- Understanding conversational context management.
- Building interactive AI applications using Streamlit.
- Learning how to deploy Python applications.

## Future Improvements

- Add document-based question answering.
- Implement long-term conversation storage.
- Add user-specific chat sessions.
- Improve chatbot response handling.
- Introduce additional LLM models.

## Author

**Kaviya Shree V.**
