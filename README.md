# PDF Chatbot

A Streamlit app that allows users to upload a PDF and interact with its content through a chatbot. Ask questions about the document via typing or speech, and receive responses, with an option to listen to the answers using text-to-speech.

## Features
- Upload a PDF and extract text.
- Ask questions based on the document.
- Type or speak questions.
- Listen to answers using text-to-speech.

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/praneethapedapudi/pdfChatbot
   cd pdfChatbot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements_local.txt
   ```

3. Run the app:
   ```bash
   streamlit run app_local.py
   ```

## Demo
[PDF Chatbot Demo](https://pdfchatbot-y9o8tm5jryzkjffv4fboqs.streamlit.app/)
This demo does not contain speech-to-text and text-to-speech functions

## Requirements

- `langchain`
- `PyMuPDF`
- `PyPDF2`
- `streamlit`
- `pandas`
- `huggingface_hub`
- `pyttsx3`
- `SpeechRecognition`
