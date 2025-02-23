import os
import json

from dotenv import load_dotenv
from django.shortcuts import render
from django.http import StreamingHttpResponse
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from .data_processing.document_loaders import get_documents_from_db
from .data_processing.prompts import prompt


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Указываем базовый URL для всех компонентов OpenAI
openai_base_url = "https://api.proxyapi.ru/openai/v1"

# Инициализация эмбеддингов с использованием прокси
embeddings = OpenAIEmbeddings(
    openai_api_key=api_key,
    openai_api_base=openai_base_url  # Кастомный URL
)


def initialize_vector_store():
    """Инициализация векторного хранилища"""
    documents = get_documents_from_db()
    return FAISS.from_texts(documents, embeddings)


# Ленивая инициализация векторного хранилища
vector_store = None


def get_vector_store():
    global vector_store
    if vector_store is None:
        vector_store = initialize_vector_store()
    return vector_store


# Инициализация модели с прокси
llm = ChatOpenAI(
    openai_api_key=api_key,
    base_url=openai_base_url,  # Используем прокси
    model="gpt-4o-mini"
)

document_chain = create_stuff_documents_chain(llm, prompt)


def generate_response_local(question):
    """Генерация ответа через LangChain с
    ленивой инициализацией векторного хранилища"""
    vs = get_vector_store()
    retriever = vs.as_retriever(search_kwargs={"k": 20})
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    try:
        response = retrieval_chain.invoke({"input": question})
        yield response["answer"]
    except Exception as e:
        yield f"Ошибка: {str(e)}"


def home(request):
    return render(request, 'index.html')


def answer(request):
    data = json.loads(request.body)
    message = data["message"]
    return StreamingHttpResponse(
        generate_response_local(message),
        content_type="text/plain"
    )
