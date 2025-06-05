# StudyBuddy: Document Q&A with Gemini AI 📚

StudyBuddy is an interactive document question-answering application that leverages Google's Gemini 2.0 Flash model to help users extract insights and information from their documents. Built with Streamlit and powered by Google's GenerativeAI, this application provides a modern, user-friendly interface for document analysis and interactive Q&A sessions.

## About 📖

StudyBuddy helps students, researchers, and professionals quickly analyze and understand their documents through natural conversation. The application uses state-of-the-art AI to process multiple document formats and maintains context throughout the conversation for more accurate and relevant responses.

## Features ✨

- **Multi-Document Support**: Upload and process multiple files simultaneously (PDF, DOCX, TXT)
- **Interactive Chat Interface**: Ask questions about your documents and get AI-powered responses
- **Conversation History**: Keep track of your Q&A session with a persistent chat history
- **Beautiful UI**: Modern and intuitive user interface with real-time processing feedback
- **Secure Processing**: Local document processing with no external storage of your data

## Prerequisites 📋

Before running the application, make sure you have:

- Python 3.7 or higher
- A Google API key for Gemini AI (obtain from [Google AI Studio](https://makersuite.google.com/app/apikey))
- Sufficient disk space for document processing
- Internet connection for API communication

### Required Python Packages
- `streamlit`: Web application framework
- `google-generativeai`: Google's Generative AI API
- `python-dotenv`: Environment variable management
- `PyPDF2`: PDF document processing
- `python-docx`: Microsoft Word document processing

## Installation 🚀

1. Clone the repository or download the source code

2. Create a virtual environment (recommended):
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install streamlit google-generativeai python-dotenv PyPDF2 python-docx
```

4. Create a `.env` file in the project root and add your Google API key:
```
GOOGLE_API_KEY=your_api_key_here
```

## Usage 💡

1. Start the application:
```bash
streamlit run app.py
```
The application will open in your default web browser at `http://localhost:8501`

2. Upload your documents:
   - Click on the file upload area
   - Select one or more supported files (PDF, DOCX, TXT)
   - Click "Process Documents"
   - Wait for the progress bar to complete

3. Ask questions:
   - Type your question in the text input field
   - Click "Ask Question" to get an AI-powered response
   - View the conversation history in the chat interface

### Example Questions

You can ask various types of questions about your documents, such as:
- "What are the main topics discussed in this document?"
- "Can you summarize the key points from all uploaded documents?"
- "Find all mentions of [specific topic] across the documents"
- "Compare and contrast the information from different documents"
- "Explain [complex concept] mentioned in the document in simpler terms"

### Best Practices

1. Document Processing:
   - Ensure PDF documents are text-searchable
   - Use clear, well-formatted documents for best results
   - Keep individual file sizes reasonable (preferably under 10MB)

2. Asking Questions:
   - Be specific in your questions
   - Start with broader questions before diving into details
   - Use follow-up questions to clarify information

3. Performance Optimization:
   - Process related documents together
   - Clear chat history for new topics
   - Consider splitting very large documents

## Supported File Types 📄

- PDF documents (*.pdf)
- Microsoft Word documents (*.docx)
- Plain text files (*.txt)

## Project Structure 📁

```
StudyBuddy/
├── app.py              # Main application file
├── .env               # Environment variables (create this)
└── README.md          # Project documentation
```

## Technical Details 🔧

### Core Functions

- `get_gemini_response(prompt, context="", history=None)`: 
  - Handles communication with the Gemini AI API
  - Maintains conversation context and history
  - Uses Gemini 2.0 Flash model for faster responses
  - Formats prompts with context for better accuracy

### Document Processing Functions

- `extract_text_from_pdf(file)`: 
  - Extracts text from PDF files using PyPDF2
  - Handles multi-page documents
  - Preserves document structure

- `extract_text_from_docx(file)`: 
  - Processes Microsoft Word documents using python-docx
  - Extracts formatted text content
  - Maintains paragraph structure

- `extract_text_from_txt(file)`: 
  - Handles plain text files
  - UTF-8 encoding support
  - Direct text extraction

- `extract_text(file)`: 
  - Main dispatcher function for file processing
  - Automatic file type detection
  - Error handling for unsupported formats

### State Management

The application uses Streamlit's session state to maintain:
- Conversation history
- Processed document content
- User interface state

## Error Handling 🛡️

The application includes error handling for:
- Missing API keys
- Unsupported file types
- API communication issues
- File processing errors

## Contributing 🤝

Feel free to contribute to this project by:
1. Forking the repository
2. Creating a new branch for your feature
3. Submitting a pull request

## Support 💬

If you encounter any issues or have questions, please open an issue in the repository.
