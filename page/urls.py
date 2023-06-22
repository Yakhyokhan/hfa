from django.urls import path, include
from .views import HtmlCreateListView
urlpatterns = [
    path('create', HtmlCreateListView.as_view())
]