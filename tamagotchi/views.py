"""
    файл со всеми views-функциями
"""

from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from tamagotchi.tasks import decrease_params


from .forms import LoginForm, RegisterForm, TamagotchiForm
from tamagotchi.models import *


def tamagotchi_images_db():
    context = {}
    context['hat'] = Hat_images.objects.all()
    context['type'] = Tamagotchi_type_images.objects.all()
    return context


@xframe_options_exempt
def main_page(request):
    """
        Функция инициализации главной страницы
    """
    return render(request, "pages/index.html")


@login_required(login_url="/authorization/")
@xframe_options_exempt
def profile_page(request):
    """
        Функция инициализации страницы профиля
    """

    context = {}
    try:
        exists_tamagotchi = Tamagotchi_Character.objects.get(
            user_owned=request.user)
    except:
        context['not_exists'] = True
        return render(request, 'pages/profile.html', context)
    look_tamagotchi = Tamagotchi_Look.objects.get(
        tamagotchi_related_to=exists_tamagotchi)
    mood_tamagotchi = Tamagotchi_Mood.objects.get(
        tamagotchi_related_to=exists_tamagotchi)
    context = {
        'tamagotchi': {
            'Tamagotchi_Character': exists_tamagotchi,
            'Tamagotchi_Look': look_tamagotchi,
            'Tamagotchi_Mood': mood_tamagotchi,
        },
        'messages': []
    }
    if mood_tamagotchi.health < 10.0:
        context['messages'].append(
            'У вашего тамагочи проблемы со здоровьем :(')
    if mood_tamagotchi.hunger < 10.0:
        context['messages'].append(
            'Тамагочи мало ел, и голодает. Покормите его')
    if mood_tamagotchi.rest < 10.0:
        context['messages'].append(
            'Тамагочи устал, уложите его спать поскорее!')
    return render(request, 'pages/profile.html', context)


@xframe_options_exempt
def sign_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'pages/login.html', {'form': form})

    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('profile')


@xframe_options_exempt
def sign_up(request):
    """
        Функция инициализации страницы регистрации и сама регистрация
    """
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'pages/register.html', {'form': form})

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('profile')
        else:
            return render(request, 'pages/register.html', {'form': form})


@login_required(login_url='/authorization/')
@xframe_options_exempt
def sign_out(request):
    """
        Функция выхода из аккаунта
    """

    logout(request)
    return redirect('main')


@login_required(login_url='/authorization/')
@xframe_options_exempt
def delete_profile_page(request):
    """
        Функция удаления профиля
    """

    exists_tamagotchi = Tamagotchi_Character.objects.get(
        user_owned=request.user)
    if exists_tamagotchi:
        Tamagotchi_Look.objects.get(
            tamagotchi_related_to=exists_tamagotchi).delete()
        Tamagotchi_Mood.objects.get(
            tamagotchi_related_to=exists_tamagotchi).delete()
        exists_tamagotchi.delete()

    request.user.delete()
    return redirect('main')


@login_required(login_url='/authorization/')
@xframe_options_exempt
def create_tamagotchi_page(request):
    """
        Функция инициализации страницы создания персонажа
    """

    context = {'pagename': 'Создать тамагочи'}
    context['images'] = tamagotchi_images_db()

    if request.method == 'GET':
        exists_tamagotchi = Tamagotchi_Character.objects.filter(
            user_owned=request.user)
        if exists_tamagotchi:
            return redirect('tamagotchi_game')

        form = TamagotchiForm()
        context['form'] = form
        return render(request, 'pages/create_tamagotchi.html', context)

    elif request.method == 'POST':
        form = TamagotchiForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            tamagotchi = Tamagotchi_Character(
                name=name, user_owned=request.user)
            tamagotchi.save()
            tamagotchi = Tamagotchi_Character.objects.get(
                user_owned=request.user)
            tamagotchi_mood = Tamagotchi_Mood(
                tamagotchi_related_to=tamagotchi
            )
            tamagotchi_look = Tamagotchi_Look(
                tamagotchi_related_to=tamagotchi,
                hat=Hat_images.objects.get(id=1),
                tamagotchi_type=Tamagotchi_type_images.objects.get(id=1)
            )
            tamagotchi_look.save()
            tamagotchi_mood.save()
            decrease_params(request.user, 300, 600, 0.1, 1.0)
            return redirect('tamagotchi_game')


@login_required(login_url='/authorization/')
@xframe_options_exempt
def custom_page(request):
    try:
        exists_tamagotchi = Tamagotchi_Character.objects.get(
            user_owned=request.user)
    except:
        return redirect('create')

    context = {'pagename': 'Изменить тамагочи'}
    context['images'] = tamagotchi_images_db()
    look_tamagotchi = Tamagotchi_Look.objects.get(
        tamagotchi_related_to=exists_tamagotchi)
    context['view'] = look_tamagotchi

    return render(request, 'pages/customise_tamagotchi.html', context)


@xframe_options_exempt
@login_required(login_url='/authorization/')
def tamagotchi_page(request):
    """
        Функция инициализации страницы с персонажем
    """

    try:
        exists_tamagotchi = Tamagotchi_Character.objects.get(
            user_owned=request.user)
    except:
        return redirect('create')

    context = {
        'pagename': 'Тамагочи',
        'tamagotchi': {
            'Tamagotchi_Character': exists_tamagotchi,
            'Tamagotchi_Look': Tamagotchi_Look.objects.get(tamagotchi_related_to=exists_tamagotchi),
            'Tamagotchi_Mood': Tamagotchi_Mood.objects.get(tamagotchi_related_to=exists_tamagotchi),
        }
    }

    return render(request, 'pages/tamagotchi.html', context)


@login_required(login_url='/authorization/')
def clicker(request):
    """
        Функция инициализации страницы с кликером
    """
    try:
        exists_tamagotchi = Tamagotchi_Character.objects.get(
            user_owned=request.user)
    except:
        return redirect('create')

    mood_tamagotchi = Tamagotchi_Mood.objects.get(
        tamagotchi_related_to=exists_tamagotchi)
    if request.method == 'POST':
        mood_tamagotchi.number_of_click += 1
        mood_tamagotchi.save(update_fields=['number_of_click'])
        data = {
            'number_of_click': mood_tamagotchi.number_of_click
        }
        return JsonResponse(data)
    context = {
        'pagename': 'Clicker',
        'mood_tamagotchi': mood_tamagotchi
    }
    return render(request, 'pages/clicker.html', context)


@login_required(login_url='/authorization/')
@xframe_options_exempt
def tamagotchi_look_change(request):
    """
         Функция изменения одежды
    """
    tamagotchi = Tamagotchi_Character.objects.get(user_owned=request.user)
    look_tamagotchi = Tamagotchi_Look.objects.get(
        tamagotchi_related_to=tamagotchi)
    if look_tamagotchi:
        try:
            query_hat = request.GET.get('hat_id', '0')
            hat = Hat_images.objects.get(id=int(query_hat))
            look_tamagotchi.hat = hat

            query_look = request.GET.get('look_id', '0')
            look = Tamagotchi_type_images.objects.get(id=int(query_look))
            look_tamagotchi.tamagotchi_type = look

            look_tamagotchi.save()
        except:
            return redirect('error')

    return redirect('tamagotchi_game')


@login_required(login_url='/authorization/')
@xframe_options_exempt
def buy_food_via_points(request):
    """
        Функция работы магазина
    """
    try:
        exists_tamagotchi = Tamagotchi_Character.objects.get(
            user_owned=request.user)
    except:
        return redirect('create')

    mood_tamagotchi = Tamagotchi_Mood.objects.get(
        tamagotchi_related_to=exists_tamagotchi)
    data = {}
    query_food = request.GET.get('food', None)
    clicks_count = mood_tamagotchi.number_of_click

    if query_food == 'cherry':
        if clicks_count < 250:
            data['error'] = 'Not enough points'
        else:
            mood_tamagotchi.number_of_click -= 250
            mood_tamagotchi.hunger = (
                85.0 if mood_tamagotchi.hunger + 5.0 > 85.0 else mood_tamagotchi.hunger + 5.0)
            mood_tamagotchi.rest = (
                0.0 if mood_tamagotchi.rest - 2.0 < 0.0 else mood_tamagotchi.rest - 2.0)
            mood_tamagotchi.health = (
                85.0 if mood_tamagotchi.health + 2.0 > 85.0 else mood_tamagotchi.health + 2.0)
    elif query_food == 'cake':
        if clicks_count < 300:
            data['error'] = 'Not enough points'
        else:
            mood_tamagotchi.number_of_click -= 300
            mood_tamagotchi.hunger = (
                85.0 if mood_tamagotchi.hunger + 7.5 > 85.0 else mood_tamagotchi.hunger + 7.5)
            mood_tamagotchi.rest = (
                0.0 if mood_tamagotchi.rest - 5.0 < 0.0 else mood_tamagotchi.rest - 5.0)
            mood_tamagotchi.health = (
                0.0 if mood_tamagotchi.health - 2.0 < 0.0 else mood_tamagotchi.health - 2.0)
    elif query_food == 'pizza':
        if clicks_count < 350:
            data['error'] = 'Not enough points'
        else:
            mood_tamagotchi.number_of_click -= 350
            mood_tamagotchi.hunger = (
                85.0 if mood_tamagotchi.hunger + 10.0 > 85.0 else mood_tamagotchi.hunger + 10.0)
            mood_tamagotchi.rest = (
                0.0 if mood_tamagotchi.rest - 4.0 < 0.0 else mood_tamagotchi.rest - 4.0)
            mood_tamagotchi.health = (
                0.0 if mood_tamagotchi.health - 3.0 < 0.0 else mood_tamagotchi.health - 3.0)
    elif query_food == 'sushi':
        if clicks_count < 150:
            data['error'] = 'Not enough points'
        else:
            mood_tamagotchi.number_of_click -= 150
            mood_tamagotchi.hunger = (
                85.0 if mood_tamagotchi.hunger + 3.0 > 85.0 else mood_tamagotchi.hunger + 3.0)
            mood_tamagotchi.rest = (
                0.0 if mood_tamagotchi.rest - 2.0 < 0.0 else mood_tamagotchi.rest - 2.0)
    elif query_food == 'tea':
        if clicks_count < 100:
            data['error'] = 'Not enough points'
        else:
            mood_tamagotchi.number_of_click -= 100
            mood_tamagotchi.hunger = (
                0.0 if mood_tamagotchi.hunger - 2.0 < 0.0 else mood_tamagotchi.hunger - 2.0)
            mood_tamagotchi.rest = (
                85.0 if mood_tamagotchi.rest + 3.0 > 85.0 else mood_tamagotchi.rest + 3.0)
            mood_tamagotchi.health = (
                85.0 if mood_tamagotchi.health + 0.5 > 85.0 else mood_tamagotchi.health + 0.5)
    else:
        data['error'] = 'Provide variable data'

    mood_tamagotchi.save()
    data['number_of_click'] = mood_tamagotchi.number_of_click
    data['tamagotchi_mood'] = {
        'health': mood_tamagotchi.health,
        'hunger': mood_tamagotchi.hunger,
        'rest': mood_tamagotchi.rest,
    }
    return JsonResponse(data)


@login_required(login_url='/authorization/')
@xframe_options_exempt
def sleep_activity_toggle(request):
    """
        Функция сна
    """
    try:
        exists_tamagotchi = Tamagotchi_Character.objects.get(
            user_owned=request.user)
    except:
        return redirect('create')

    mood_tamagotchi = Tamagotchi_Mood.objects.get(
        tamagotchi_related_to=exists_tamagotchi)
    data = {}
    if mood_tamagotchi.is_in_rest:
        mood_tamagotchi.is_in_rest = False
        mood_tamagotchi.save()
        data = {
            'code': 2,
            'message': 'Rest stopped',
        }
    else:
        if mood_tamagotchi.rest < 85.0:
            mood_tamagotchi.is_in_rest = True
            mood_tamagotchi.save()
            data = {
                'code': 1,
                'message': 'Rest started',
            }
        else:
            data = {
                'code': 3,
                'message': 'Rest is allready full',
            }

    return JsonResponse(data)


@login_required(login_url='/authorization/')
@xframe_options_exempt
def get_stats(request):
    """
        Функция получения характеристик персонажа
    """
    try:
        exists_tamagotchi = Tamagotchi_Character.objects.get(
            user_owned=request.user)
    except:
        return redirect('create')

    mood_tamagotchi = Tamagotchi_Mood.objects.get(
        tamagotchi_related_to=exists_tamagotchi)
    data = {
        'health': mood_tamagotchi.health,
        'hunger': mood_tamagotchi.hunger,
        'rest': mood_tamagotchi.rest,
    }

    return JsonResponse(data)
