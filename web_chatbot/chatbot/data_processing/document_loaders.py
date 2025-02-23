from ..models import Cat, Owner, Dog


def get_documents_from_db():
    """Получаем данные из базы данных"""
    documents = []

    # Обрабатываем владельцев
    owners = Owner.objects.prefetch_related('known_owners').all()
    for owner in owners:
        known_owners = ", ".join(
            [f"{o.first_name} {o.last_name}" for o in owner.known_owners.all()]
            )
        doc = (
            f"Владелец: {owner.first_name} {owner.last_name}\n"
            f"Пол: {owner.get_gender_display()}\n"
            f"Телефон: {owner.phone_number}\n"
            f"Лет знакомства: {owner.years_known}\n"
            f"Знаком с: {known_owners if known_owners else 'никем'}"
        )
        documents.append(doc)

    # Обрабатываем кошек
    cats = Cat.objects.select_related('owner').all()
    for cat in cats:
        owner_info = (
            f"{cat.owner.first_name} {cat.owner.last_name}"
            if cat.owner
            else "неизвестен"
            )
        doc = (
            f"Тип: Кошка\n"
            f"Кличка: {cat.name}\n"
            f"Возраст: {cat.age}\n"
            f"Цвет: {cat.color}\n"
            f"Владелец: {owner_info}"
        )
        documents.append(doc)

    # Обрабатываем собак
    dogs = Dog.objects.select_related('owner').all()
    for dog in dogs:
        owner_info = (
            f"{dog.owner.first_name} {dog.owner.last_name}"
            if dog.owner
            else "неизвестен"
            )
        doc = (
            f"Тип: Собака\n"
            f"Кличка: {dog.name}\n"
            f"Возраст: {dog.age}\n"
            f"Порода: {dog.breed}\n"
            f"Владелец: {owner_info}"
        )
        documents.append(doc)

    return documents
