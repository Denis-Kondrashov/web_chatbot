from django.db import models


class Cat(models.Model):
    name = models.CharField(max_length=50, verbose_name="Кличка")
    age = models.IntegerField(verbose_name="Возраст")
    color = models.CharField(max_length=30, verbose_name="Цвет")

    def __str__(self):
        return f"{self.name} ({self.color}, {self.age} лет)"
