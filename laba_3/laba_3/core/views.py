from django.shortcuts import render
from rest_framework import viewsets
from .models import File
from .serializers import FileSerializer
# Create your views here.


class FileView(viewsets.ModelViewSet):
    queryset = File.objects.all().order_by('id')
    serializer_class = FileSerializer

