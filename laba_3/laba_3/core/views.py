from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from .models import File
from .serializers import FileSerializer
# Create your views here.


class FileView(viewsets.ModelViewSet):
    queryset = File.objects.all().order_by('id')
    serializer_class = FileSerializer

    @staticmethod
    def create(request):
        print(request.FILES)
        print(request.data)
        name = request.data['name']
        file = request.data['file']
        File.objects.create(name=name, file=file)
        return JsonResponse({
            'status': 200
        })

