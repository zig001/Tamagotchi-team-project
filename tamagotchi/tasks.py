from celery import shared_task
from django.contrib.auth.models import User
from tamagotchi.models import Tamagotchi_Character, Tamagotchi_Mood
from time import sleep
from random import randint, uniform


@shared_task
def decrease_params(user, left_time_border, right_time_border, left_border, right_border):
    character = Tamagotchi_Character.objects.get(user_owned=user)
    try:
        mood = Tamagotchi_Mood.objects.get(tamagotchi_related_to=character)
    except:
        print('Tamagotchi_Mood does not exists for this user!')
    else:
        while True:
            rest_fl = randint(0, 1)
            hunger_fl = randint(0, 1)
            sleep(randint(left_time_border, right_time_border))
            if mood.is_in_rest:
                change = round(uniform(left_border, right_border), 1)  
                if mood.rest + change > 85:
                    mood.rest = 85
                else:
                    mood.rest += change

                change = round(uniform(left_border, right_border), 1)
                if mood.hunger - change < 0:
                    mood.hunger = 0
                else:
                    mood.hunger -= change
            elif rest_fl:
                change = round(uniform(left_border, right_border), 1)
                if mood.rest == 0:
                    mood.health -= 0.5
                else:
                    if mood.rest - change < 0:
                        mood.rest = 0
                    else:
                        mood.rest -= change
            if hunger_fl:
                change = round(uniform(left_border, right_border), 1)
                if mood.hunger == 0:
                    mood.health -= 0.5
                else:
                    if mood.hunger - change < 0:
                        mood.hunger = 0
                    else:
                        mood.hunger -= change
            mood.save()
