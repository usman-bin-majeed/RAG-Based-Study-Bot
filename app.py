import streamlit as st
import google.generativeai as genai
import os
import tempfile
import PyPDF2
import docx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("Google API Key not found! Please set the GOOGLE_API_KEY environment variable.")
    GOOGLE_API_KEY = ""  # Set to empty string to avoid None errors

genai.configure(api_key=GOOGLE_API_KEY)

# Format instructions mapping
FORMAT_INSTRUCTIONS = {
    "Answer like a teacher": "Explain the answer in a teaching style, as if instructing a student. Break down complex concepts into simpler terms and provide clear explanations.",
    "Summarize the answer": "Provide a concise summary of the answer, focusing on the key points and main ideas. Keep it brief but comprehensive.",
    "Add examples": "Include relevant, practical examples to illustrate the answer. Use real-world scenarios to demonstrate the concept.",
    "Use bullet points": "Present the answer using clear, organized bullet points. Structure the information for easy readability."
}

def get_gemini_response(prompt, context="", history=None, format_instruction=""):
    """Get response from Gemini model with context, history, and format instruction"""
    if not history:
        history = []
    
    # Format history into conversation format
    formatted_history = "\n\n".join([f"User: {h['user']}\nAssistant: {h['assistant']}" for h in history])
    
    # Create the complete prompt
    full_prompt = f"""
    Context information:
    {context}
    
    Previous conversation:
    {formatted_history}
    
    User question: {prompt}
    
    {format_instruction}
    
    Please answer the question based on the provided context and previous conversation.
    """
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        error_message = f"Error calling Gemini API: {str(e)}"
        st.error(error_message)
        return f"I encountered an error: {error_message}. Please check your API key and try again."

def extract_text_from_pdf(file):
    """Extract text from a PDF file"""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        temp_file.write(file.getvalue())
        temp_path = temp_file.name
    
    text = ""
    with open(temp_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text() + "\n"
    
    os.unlink(temp_path)
    return text

def extract_text_from_docx(file):
    """Extract text from a DOCX file"""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as temp_file:
        temp_file.write(file.getvalue())
        temp_path = temp_file.name
    
    doc = docx.Document(temp_path)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    
    os.unlink(temp_path)
    return text

def extract_text_from_txt(file):
    """Extract text from a TXT file"""
    return file.getvalue().decode("utf-8")

def extract_text(file):
    """Extract text based on file type"""
    file_type = file.name.split('.')[-1].lower()
    
    if file_type == 'pdf':
        return extract_text_from_pdf(file)
    elif file_type == 'docx':
        return extract_text_from_docx(file)
    elif file_type == 'txt':
        return extract_text_from_txt(file)
    else:
        st.error(f"Unsupported file type: {file_type}")
        return ""

def main():
    st.set_page_config(page_title="Document Q&A with Gemini", page_icon="📚")
    
    st.title("Chat with Your Documents 📚")
    st.subheader("Upload documents and ask questions")
    
    # Initialize session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'document_text' not in st.session_state:
        st.session_state.document_text = ""
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Upload PDF, DOCX, or TXT files", 
        accept_multiple_files=True,
        type=['pdf', 'docx', 'txt']
    )
    
    # Process uploaded files
    if uploaded_files and st.button("Process Documents"):
        combined_text = ""
        for file in uploaded_files:
            st.info(f"Processing {file.name}...")
            file_text = extract_text(file)
            combined_text += f"\n\n--- Document: {file.name} ---\n{file_text}"
        
        st.session_state.document_text = combined_text
        st.success("Documents processed successfully!")
    
    # Chat interface
    st.subheader("Ask about your documents")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for chat in st.session_state.chat_history:
            st.markdown(f"**You:** {chat['user']}")
            st.markdown(f"**Assistant:** {chat['assistant']}")
    
    # User input and format selection
    user_question = st.text_input("Type your question here:")
    answer_format = st.selectbox(
        "Select answer format",
        options=list(FORMAT_INSTRUCTIONS.keys()),
        index=0
    )
    
    if user_question and st.session_state.document_text:
        if st.button("Ask"):
            with st.spinner("Thinking..."):
                format_instruction = FORMAT_INSTRUCTIONS[answer_format]
                response = get_gemini_response(
                    user_question, 
                    st.session_state.document_text,
                    st.session_state.chat_history,
                    format_instruction
                )
                
                # Add to history
                st.session_state.chat_history.append({
                    "user": f"{user_question} [Format: {answer_format}]",
                    "assistant": response
                })
                
                st.rerun()
    
    elif user_question and not st.session_state.document_text:
        st.warning("Please upload and process documents first!")

if __name__ == "__main__":
    main()
