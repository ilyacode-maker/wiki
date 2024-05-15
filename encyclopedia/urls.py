from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.get_entry_page, name='get_entry_page'),
    path("search", views.search, name='search'),
    path("new_page", views.new_page, name='create'),
    path("random", views.random_page, name='random')
]