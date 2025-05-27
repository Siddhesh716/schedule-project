from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name=""),
    path("schedule_view/", views.schedule_view, name='schedule_view'),
]