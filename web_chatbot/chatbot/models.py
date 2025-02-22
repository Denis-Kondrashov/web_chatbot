from django.db import models


class Owner(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    phone_number = models.CharField(max_length=15, verbose_name="Номер телефона", blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Cat(models.Model):
    name = models.CharField(max_length=50, verbose_name="Кличка")
    age = models.IntegerField(verbose_name="Возраст")
    color = models.CharField(max_length=30, verbose_name="Цвет")
    owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, verbose_name="Владелец", null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.color}, {self.age} лет) {self.owner}"

