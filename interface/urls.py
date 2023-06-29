from django.urls import path
from .views import HtmlCreateView, HtmlDetailView
urlpatterns = [
    path('create', HtmlCreateView.as_view(), name= "html_create"),
    path('<int:pk>', HtmlDetailView.as_view(), name= "html_detail")
]