import os
from dotenv import load_dotenv
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import openai

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(
    api_key=api_key,
    base_url="https://api.proxyapi.ru/openai/v1",
)


def home(request):
    """
    Представление для отображения главной страницы.
    """
    return render(request, 'index.html')


@require_POST
def ask_question(request):
    question = request.POST.get('question', '')

    if not question:
        return JsonResponse({'error': 'Вопрос не может быть пустым.'}, status=400)

    try:
        # Отправляем запрос в OpenAI через объект client
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": question}],
            temperature=0.7,
            max_tokens=256,
        )

        response = completion.choices[0].message.content
        return JsonResponse({'response': response}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
