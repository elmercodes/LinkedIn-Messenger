from llama_index.core import SummaryIndex
from llama_index.readers.file import HTMLTagReader
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.llms.openai import OpenAI
import tempfile
import os 
from dotenv import load_dotenv
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


with st.sidebar:
    st.title("LinkedIn Profile Messenger")
    st.markdown('''
    ## About
    
    Upload your profile as well as the other person's profile and prompt the chatbot to generate messages.
    For example you can ask the chat bot 'Send a brief freindly introductory message from me(your name) to (person's profile) asking to
    learn more about them and their experiences. Make sure to mention mutual interests/expereinces.'
    
                ''')
    add_vertical_space(5)
    st.write("If you changed any of the below or wish to upload a different profile after you send your initial message"
             ", make sure you go to the top right with the 3 vertical dots and hit 'Rerun' for best use.")
    model = st.sidebar.selectbox("Choose the model", ["gpt-3.5-turbo", "gpt-4-0125-preview"])
    temperature = st.sidebar.slider("Select temperature", 0.0, 1.0, 0.7)

def save_uploaded_file(uploaded_files):
    temp_dir = tempfile.mkdtemp()
    saved_paths = []
    # Check if uploaded_files is a list and has at least one file
    if uploaded_files and isinstance(uploaded_files, list):
        for uploaded_file in uploaded_files:
            file_path = os.path.join(temp_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            saved_paths.append(file_path)
    elif uploaded_files:  # Single file object
        file_path = os.path.join(temp_dir, uploaded_files.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_files.getbuffer())
        saved_paths.append(file_path)

    return saved_paths


def main():
    st.header("Craft Messages for LinkedIn Profiles")
    uploaded_files = st.file_uploader("Go to the LinkedIn page/profile you want to message. For Windows/Linux hit (Ctrl + S) to save the page, "
                                     "for Mac (Command + S). Afterwards, upload the file here.", accept_multiple_files=True)

    if uploaded_files:
        saved_file_paths = save_uploaded_file(uploaded_files)
        combined_documents = []

        for file_path in saved_file_paths:
            reader = HTMLTagReader(tag="section", ignore_no_id=False)
            documents = reader.load_data(file_path)
            combined_documents.extend(documents)  # Combining documents from all files

        if combined_documents:
            index = SummaryIndex.from_documents(combined_documents)
            memory = ChatMemoryBuffer.from_defaults(token_limit=40000)

            system_prompt = (
                "You are a chatbot whose responsibility is to help craft carefully written messages to people on LinkedIn, "
                "using the uploaded HTML files to learn more about the user and the person being written to. "
                "Help the user craft a message in the manner they see fit."
            )
            chat_engine = index.as_chat_engine(
                chat_mode="context",
                llm=OpenAI(model=model),
                memory=memory,
                system_prompt=system_prompt,
                temperature=temperature
            )

            if "messages" not in st.session_state:
                st.session_state.messages = []

            # Display existing conversation
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.write(message["content"])

            # Capture new user input
            prompt = st.chat_input("Craft a message:")

            if prompt:
                st.session_state.messages.append({"role": "user", "content": prompt})
                # Concatenate all messages to form the full conversation context
                full_conversation = " ".join([msg["content"] for msg in st.session_state.messages])
                
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        # The chat engine uses the full conversation for context
                        response = chat_engine.chat(full_conversation)
                        st.write(response.response)
                        st.session_state.messages.append({"role": "assistant", "content": response.response})

if __name__ == "__main__":
    main()