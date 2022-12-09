from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name='search'),
    path("new/", views.new_page, name = "new_page"),
    path("edit/<str:title>", views.edit, name = "edit"),
    path("random/", views.rand, name = "rand"),
    path("wiki/<str:title>", views.entry_page, name = "entry_page")
]
