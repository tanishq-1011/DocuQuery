
---

# 🧠 PDF Conversational Retrieval App with Chainlit

This project demonstrates a **Conversational Retrieval System** that allows users to upload PDF files and interact with the content using natural language questions. Powered by **LangChain**, **OllamaEmbeddings**, **PyPDF2**, **Chroma**, and **Chainlit**, the app extracts text from PDFs, converts it into chunks, creates a vector store for efficient retrieval, and uses conversational models to answer user questions about the PDF content.

---

## 🚀 Features

- **PDF Upload**: Users can easily upload PDF files up to **100MB** and interact with the content in a user-friendly way.
- **Text Splitting**: PDF content is chunked into manageable parts using a customizable character splitter.
- **Conversational AI**: The app integrates **ChatOllama** and **ChatGroq** models for seamless conversational interaction with the uploaded PDF.
- **Chroma Vector Store**: The app uses the Chroma vector store for efficient document retrieval based on user queries.
- **Memory Management**: Maintains conversational history and context using **ConversationBufferMemory**, making the interaction feel natural.
- **Source Document Retrieval**: Retrieves and shows source documents related to the user's queries for transparency.

---

## 📦 Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/your-repo.git
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**:

   Simply execute:

   ```bash
   chainlit run app.py
   ```

   The app will start on the default **localhost:8000**.

---

## 📝 Usage

1. **Upload a PDF**: Upon app start, the system will prompt you to upload a PDF file.
2. **Ask Questions**: Once the file is processed, you can interact with the PDF content by typing your questions.
3. **Get Answers & Sources**: The app will provide answers along with referenced source documents from the PDF, making it easy to verify the information.

---

## 🌟 Example Flow

1. **Upload a PDF**:
   - The app prompts: `"Please upload a PDF file to begin!"`
   - After selecting a PDF file, you will see the message: `"Processing 'filename.pdf'..."`

2. **Interact with the PDF**:
   - You ask: `"What is the summary of chapter 2?"`
   - The app responds with a relevant answer and indicates the source page(s) from the PDF.

---


## 🤝 Contributing

Feel free to fork this repository, create issues, or submit pull requests. Any contributions that enhance the functionality or add more models are welcome!

---


Let me know if you'd like to adjust anything!
