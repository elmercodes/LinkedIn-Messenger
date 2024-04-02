# LinkedIn Messenger

LinkedIn Messenger is a tool that leverages the power of large language models (LLMs) like GPT-3.5 and GPT-4 to help users craft personalized and engaging messages for LinkedIn profiles. The app analyzes uploaded LinkedIn profiles to generate messages that can include friendly introductions, networking requests, or other professional communication tailored to the shared interests and experiences between two individuals.

## Features

- **Profile Analysis**: Upload LinkedIn profiles to understand key details and interests.
- **Custom Message Generation**: Utilize advanced LLMs to generate context-aware, personalized messages for LinkedIn outreach.
- **Model and Temperature Selection**: Choose from different AI models and set the temperature to control the creativity and style of the generated messages.

## Getting Started

### Prerequisites

- Python 3.8+
- Streamlit
- llama-index
- OpenAI API key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/linkedin-messenger.git
   cd linkedin-messenger
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
3. Set up your .env file with the necessary environment variables, including your OpenAI API key:
   ```bash
   OPENAI_API_KEY='your_openai_api_key_here'
   
### Usage

1. Start the Streamlit app:
   ```bash
   streamlit run app.py
2. Open your web browser to http://localhost:8501 to use the application.

3. Follow the on-screen instructions to upload LinkedIn profiles and generate messages.

## How It Works

The application uses Streamlit for the user interface, where users can upload HTML files of LinkedIn profiles. The backend, powered by the llama-index library, processes these files to extract meaningful information that the OpenAI model uses to craft messages tailored to the specific context of the uploaded profiles.

### Configuration

- **Model Selection**: Choose between GPT-3.5 Turbo and GPT-4 models based on your needs and API access.
- **Temperature Setting**: Adjust the temperature to control the variance in the generated messages, with higher temperatures resulting in more creative outputs.

### Contributing

Contributions to LinkedIn Messenger are welcome! Feel free to fork the repository, make changes, and submit pull requests.

### License

This project is licensed under the [MIT License](LICENSE).

### Disclaimer

This tool is for educational and professional networking purposes. Please ensure that all communications through LinkedIn comply with LinkedIn's terms of service and respect user privacy and data usage policies.
