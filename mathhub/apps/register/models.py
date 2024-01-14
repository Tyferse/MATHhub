from django.db import models
from django.contrib.auth.models import User


class LivePlace(models.Model):
    CHOICES = (
        ("Отсутствует", "Отсутствует"),
        ("Кампус", "Кампус"),
        ("Город", "Город"),
        ("Подвал", "Подвал"),
        ("Под мостом", "Под мостом")
    )
    place = models.CharField("Предпочитаемое место жительства",
                             max_length=20, choices=CHOICES)
    

class ChosenIntegral(models.Model):
    CHOICES = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
    )
    integral = models.IntegerField("Выбранные интегралы",
                                   choices=CHOICES)


class ProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_math = models.BooleanField("Математик?")
    live_place = models.ForeignKey(LivePlace, on_delete=models.CASCADE)
    chosen_integrals = models.ManyToManyField(ChosenIntegral)


class Subscription(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email
