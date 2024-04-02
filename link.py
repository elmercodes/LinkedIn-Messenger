from llama_index.core import SummaryIndex
from llama_index.readers.web import SimpleWebPageReader
# from IPython.display import Markdown, display
import os
from dotenv import load_dotenv
from llama_index.core import SummaryIndex
from llama_index.readers.file import HTMLTagReader
from llama_index.core.memory import ChatMemoryBuffer
import subprocess
import os
import glob
import requests
from dotenv import load_dotenv
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


def save_html(url):
    try:
        # Command to download the entire webpage and its assets
        command = ["wget", "-p", "-k", "-E", url]

        # Run the command
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Find the most recently downloaded .html file in the current directory
        list_of_files = glob.glob('./*.html')  # list all html files in the current directory
        latest_file = max(list_of_files, key=os.path.getctime)

        print(f"Webpage downloaded successfully: {url}")
        print(f"Saved as: {latest_file}")

        return latest_file  # Return the name of the saved file
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while downloading the webpage: {e}")
        return None
    
file_name = save_html("https://www.linkedin.com/in/jeremy-allen-jacobson/")

reader = HTMLTagReader(tag="section", ignore_no_id=False)
documents = reader.load_data(f"./{file_name}")
index = SummaryIndex.from_documents(documents)
# memory = ChatMemoryBuffer.from_defaults(token_limit=40000)

# chat_engine = index.as_chat_engine(
#     chat_mode="context",
#     memory=memory,
#     system_prompt=(
#         "You are a chatbot whose responsibility is to help craft carefully written messages to people on LinkedIn, "
#         "using the uploaded HTML file to learn more about the person being written to. Help the user craft a message."
#     ),
# )



# chat_engine = index.as_chat_engine()
# response = chat_engine.query("tell me about this profile")

# print(response)
