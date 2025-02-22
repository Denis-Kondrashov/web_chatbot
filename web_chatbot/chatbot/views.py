import os
import json
from dotenv import load_dotenv
from django.shortcuts import render
from django.http import StreamingHttpResponse
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from .models import Cat, Owner

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Важно: Указываем базовый URL для всех компонентов OpenAI
openai_base_url = "https://api.proxyapi.ru/openai/v1"

# Инициализация эмбеддингов с прокси
embeddings = OpenAIEmbeddings(
    openai_api_key=api_key,
    openai_api_base=openai_base_url  # Добавляем кастомный URL
)

def get_documents_from_db():
    """Получаем данные из SQLite"""
    documents = []
    cats = Cat.objects.select_related('owner').all()
    
    for cat in cats:
        doc = (
            f"Кличка: {cat.name}\n"
            f"Возраст: {cat.age}\n"
            f"Цвет: {cat.color}\n"
            f"Владелец: {cat.owner.first_name} {cat.owner.last_name}\n"
            f"Телефон: {cat.owner.phone_number}"
        )
        documents.append(doc)
    return documents

# Создаем векторное хранилище (перенесем инициализацию внутрь функции)
def initialize_vector_store():
    documents = get_documents_from_db()
    return FAISS.from_texts(documents, embeddings)

vector_store = initialize_vector_store()
retriever = vector_store.as_retriever(search_kwargs={"k": 20})

# Инициализация модели с прокси
llm = ChatOpenAI(
    openai_api_key=api_key,
    base_url=openai_base_url,  # Используем ваш прокси
    model="gpt-4o-mini"
)

prompt = ChatPromptTemplate.from_template(
    """Ты аналитик базы данных кошек. Отвечай ТОЛЬКО на основе контекста. 
    Если нужно посчитать количество, проведи полный анализ всех данных в контексте.

    Контекст:
    {context}

    Вопрос: {input}"""
)

document_chain = create_stuff_documents_chain(llm, prompt)
retrieval_chain = create_retrieval_chain(retriever, document_chain)

def generate_response(question):
    """Генерация ответа через LangChain"""
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
        generate_response(message), 
        content_type="text/plain"
    )