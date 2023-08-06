from django.urls import path

from .views import viewAuth

urlpatterns = [
    path('auth/', viewAuth, name="ssoauth"),

]
