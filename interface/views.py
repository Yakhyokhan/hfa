from django.shortcuts import render
from .serializer import HtmlSerializer
from rest_framework import generics
from .models import Html

# Create your views here.

class HtmlCreateView(generics.CreateAPIView):
    queryset = Html.objects.all()
    serializer_class = HtmlSerializer

class HtmlDetailView(generics.RetrieveAPIView):
    queryset = Html.objects.all()
    serializer_class = HtmlSerializer