import streamlit as st
import io, re
import fitz
import pyttsx3
import speech_recognition as sr
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain import HuggingFaceHub

# Initialize Langchain LLM
llm = HuggingFaceHub(repo_id="mistralai/Mistral-7B-Instruct-v0.2", model_kwargs={"temperature": 0.5, "max_new_tokens": 4000},
                     huggingfacehub_api_token="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")

# Function to extract text from uploaded PDF
def extract_text_from_pdf(uploaded_file):
    try:
        pdf_file = uploaded_file.read()
        doc = fitz.open("pdf", pdf_file)
        text = ""
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text += page.get_text()

        return text

    except Exception as e:
        return f"Error: {e}"

# Function to generate Q&A based on PDF content using Langchain
def generate_answer_based_on_pdf(text, query):
    prompt = PromptTemplate(
        input_variables=["text", "query"], 
        template="Based on the following document content:\n{text}\n\nAnswer the user's question succinctly:\n\nUser's Query: {query}\nAnswer:"
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run({"text": text, "query": query})
    return response.strip()

# Function to filter out the PDF content from the model's response
def filter_pdf_content_from_response(response, pdf_text):
    return re.split(r'(?<=[.!?])\s+', response.replace(pdf_text, "").strip())[-1]

# Function to convert text to speech
# def text_to_speech(text):
#     engine = pyttsx3.init()
#     engine.say(text)
#     engine.runAndWait()


# # Function to convert speech to text
# def speech_to_text():
#     recognizer = sr.Recognizer()
#     microphone = sr.Microphone()

#     with microphone as source:
#         st.write("Listening... Please speak your question.")
#         recognizer.adjust_for_ambient_noise(source)
#         audio = recognizer.listen(source)

#     try:
#         st.write("Converting speech to text...")
#         query = recognizer.recognize_google(audio)
#         st.write(f"You asked: {query}")
#         return query
#     except sr.UnknownValueError:
#         st.error("Sorry, I could not understand the speech.")
#         return None
#     except sr.RequestError:
#         st.error("Sorry, there was an error with the speech recognition service.")
#         return None


# Streamlit UI setup
st.title("PDF Chatbot")
st.sidebar.header("Upload PDF")
uploaded_file = st.sidebar.file_uploader("Upload your PDF file", type=["pdf"])

if "conversation" not in st.session_state:
    st.session_state.conversation = []

if uploaded_file is not None:
    text = extract_text_from_pdf(uploaded_file)
    if text.startswith("Error:"):
        st.sidebar.error("Failed to process the PDF. Please try again with a valid file.")
    else:
        st.sidebar.success("PDF uploaded and processed successfully!")
        st.subheader("Chat with the PDF")
        if st.session_state.conversation:
            for qna in st.session_state.conversation:
                st.write(f"**Q:** {qna['question']}")
                st.write(f"**A:** {qna['answer']}")

        user_query = None
        input_method = st.radio("How would you like to ask your question?", ("Type", "Speak"))

        if input_method == "Type":
            user_query = st.text_input("Type your question based on the PDF content:")

        elif input_method == "Speak":
            if st.button("Speak Question"):
                user_query = speech_to_text()

        if user_query:
            raw_response = generate_answer_based_on_pdf(text, user_query)
            filtered_response = filter_pdf_content_from_response(raw_response, text)
            st.session_state.conversation.append({"question": user_query, "answer": filtered_response})
            st.write(filtered_response)
            if st.button("Speak Answer"):
                text_to_speech(filtered_response)
                
else:
    st.sidebar.warning("Please upload a PDF file to begin.")
