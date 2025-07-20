"""
    файл с классами для ипортов
"""

from django.contrib.auth.models import User
from django.db import models


# https://dbdiagram.io/d/Thamagochi-65d2314dac844320ae68c9cd
class Tamagotchi_Character(models.Model):
    """
    Класс описания тамагочи, в нем представлена общая информации о тамагочи.
    Также служит для сочетания пользователя и характеристик.

    :param user_owned: Ссылка на класс пользователя(django.contrib.auth.models.User), к которому привязан Тамагочи.
    :param name: Имя тамагочи.
    :param date_created: Время создания тамагочи.
    """

    user_owned = models.OneToOneField(to=User, on_delete=models.CASCADE)

    name = models.CharField(null=False, max_length=32)
    date_created = models.DateTimeField(auto_now_add=True)


class Tamagotchi_Mood(models.Model):
    """
    Класс описывающий характеристики тамагочи.

    :param tamagotchi_related_to: Ссылка на класс тамагочи(models.TamagotchiCharacter), к которому привязаны характеристики.
    :param health: Здоровье тамагочи
    :param hunger: Голод тамагочи
    :param number_of_click: количество кликов(валюты)
    :param rest: Бодрость тамагочи
    """

    tamagotchi_related_to = models.OneToOneField(
        to=Tamagotchi_Character, on_delete=models.CASCADE
    )

    health = models.FloatField(null=False, default=85.0)
    hunger = models.FloatField(null=False, default=85.0)
    rest = models.FloatField(null=False, default=85.0)
    is_in_rest = models.BooleanField(null=False, default=False)
    number_of_click = models.IntegerField(null=False, default=0)


class Hat_images(models.Model):
    """
    Таблица для хранения картинок шляп

    :param image: картинка для шляпки
    """

    image = models.ImageField(upload_to="images")


class Tamagotchi_type_images(models.Model):
    """
    Таблица для хранения картинок видов тамагочи

    :param image: картинка для тамагочи
    """

    image = models.ImageField(upload_to="images")


class Tamagotchi_Look(models.Model):
    """
    Класс описывающий одежду тамагочи. hat_choice и tshirt_choice - id одежды

    :param tamagotchi_related_to: Ссылка на класс тамагочи(models.TamagotchiCharacter), к которому привязан вид.
    :param hat: Cсылка на класс шляп(models.Hat_images), в котором хранится текущая шляпка.
    :param tamagotchi_type: Cсылка на класс шляп(models.Tshirt_images), в котором хранится текущий вид тамагочи.
    """

    tamagotchi_related_to = models.OneToOneField(
        to=Tamagotchi_Character, on_delete=models.CASCADE
    )

    hat = models.ForeignKey(to=Hat_images, on_delete=models.CASCADE)
    tamagotchi_type = models.ForeignKey(
        to=Tamagotchi_type_images, on_delete=models.CASCADE
    )
