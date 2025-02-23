from langchain_core.prompts import ChatPromptTemplate


prompt = ChatPromptTemplate.from_template(
    """Ты аналитик базы данных домашних животных.
    Отвечай ТОЛЬКО на основе контекста.
Учитывай следующее:
- В базе есть кошки и собаки
- У каждого животного есть владелец
- Владельцы имеют связи между собой

Контекст:
{context}

Вопрос: {input}"""
)
