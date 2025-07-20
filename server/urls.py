"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from server import settings
from tamagotchi import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.main_page, name="main"),
    path("registration/", views.sign_up, name="register"),
    path("authorization/", views.sign_in, name="login"),
    path("sign_out/", views.sign_out, name="sign_out"),
    path("profile/", views.profile_page, name="profile"),
    path("delete_profile/", views.delete_profile_page),
    path("create_tamagotchi/", views.create_tamagotchi_page, name="create"),
    path("tamagotchi/", views.tamagotchi_page, name="tamagotchi_game"),
    path("customize/", views.custom_page, name="custom"),
    path("clicker/", views.clicker, name="clicker"),
    path("api/tamagotchi_look_change", views.tamagotchi_look_change),
    path("api/buy_food", views.buy_food_via_points),
    path("api/rest_activity", views.sleep_activity_toggle),
    path("api/get_stats", views.get_stats),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
