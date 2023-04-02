from django.urls import path

from api.views.views import main_page, generate_page, result_search, generate_index, parse_html

urlpatterns = [
    path("", main_page, name="main"),
    path('generate/', generate_page, name="generate"),
    path('search/', result_search, name="search"),
    path('generate_index/', generate_index, name="generate_index"),
    path('generate_html/', parse_html, name="generate_html")
]