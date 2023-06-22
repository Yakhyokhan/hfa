from django.urls import path
from .views import HtmlCreateView, HtmlDetailView
urlpatterns = [
    path('create', HtmlCreateView.as_view(), name= "html-create"),
    path('<int:pk>', HtmlDetailView.as_view(), name= "html-detail")
]