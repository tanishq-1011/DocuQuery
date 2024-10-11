import PyPDF2
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOllama
from langchain_groq import ChatGroq
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
import chainlit as cl

# LLM initialization
local_llm = ChatOllama(model="mistral:instruct")
groq_llm = ChatGroq(model_name="mixtral-8x7b-32768")

# Chat handler
@cl.on_chat_start
async def initiate_chat():
    uploaded_files = None  # Placeholder for file storage

    # Prompt user to upload a file
    while not uploaded_files:
        uploaded_files = await cl.AskFileMessage(
            content="Upload a PDF to get started!",
            accept=["application/pdf"],
            max_size_mb=100,
            timeout=180
        ).send()

    uploaded_file = uploaded_files[0]  # Access the first uploaded file

    # Inform the user that the file is being processed
    processing_message = cl.Message(content=f"Processing your file: `{uploaded_file.name}` ...")
    await processing_message.send()

    # Read the uploaded PDF file
    pdf_reader = PyPDF2.PdfReader(uploaded_file.path)
    pdf_content = "".join([page.extract_text() for page in pdf_reader.pages])

    # Split the text for efficient chunking and embedding
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_texts = splitter.split_text(pdf_content)

    # Associate metadata with each chunk
    metadata = [{"source": f"{idx}-pl"} for idx in range(len(split_texts))]

    # Create a Chroma vector store using the embeddings model
    embedder = OllamaEmbeddings(model="nomic-embed-text")
    docsearch = await cl.make_async(Chroma.from_texts)(split_texts, embedder, metadatas=metadata)

    # Initialize chat memory to maintain conversation context
    chat_memory = ChatMessageHistory()

    # Create memory buffer for the conversation
    conversation_memory = ConversationBufferMemory(
        memory_key="conversation_history",
        output_key="response",
        chat_memory=chat_memory,
        return_messages=True
    )

    # Set up a conversational retrieval chain that uses the vector store for querying
    retrieval_chain = ConversationalRetrievalChain.from_llm(
        llm=local_llm,
        retriever=docsearch.as_retriever(),
        memory=conversation_memory,
        return_source_documents=True
    )

    # Let the user know the system is ready for queries
    processing_message.content = f"Processing completed for `{uploaded_file.name}`. You may now ask questions!"
    await processing_message.update()

    # Store the chain in the user session for later use
    cl.user_session.set("retrieval_chain", retrieval_chain)


# Message handling function for chat interaction
@cl.on_message
async def handle_message(message: cl.Message):
    retrieval_chain = cl.user_session.get("retrieval_chain")
    callback_handler = cl.AsyncLangchainCallbackHandler()

    # Invoke the retrieval chain with the user's message
    response = await retrieval_chain.ainvoke(message.content, callbacks=[callback_handler])
    answer = response["answer"]
    source_documents = response["source_documents"]

    # Prepare the response message and source references
    text_elements = []
    if source_documents:
        for idx, document in enumerate(source_documents):
            source_label = f"source_{idx}"
            text_elements.append(cl.Text(content=document.page_content, name=source_label))

        source_names = [element.name for element in text_elements]
        answer += f"\nSources: {', '.join(source_names)}" if source_names else "\nNo sources found."

    # Send the final message with the answer and any relevant sources
    await cl.Message(content=answer, elements=text_elements).send()
