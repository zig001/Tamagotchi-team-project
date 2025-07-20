from django.contrib import admin
from tamagotchi.models import *

# Register your models here.

"""
Superuser

username: vasya
password: 123
"""

admin.site.register(Tamagotchi_Character)
admin.site.register(Tamagotchi_Mood)
admin.site.register(Hat_images)
admin.site.register(Tamagotchi_type_images)
admin.site.register(Tamagotchi_Look)
