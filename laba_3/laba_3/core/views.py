from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from .models import File, ExpertSystem
from .serializers import FileSerializer
# Create your views here.


class FileView(viewsets.ModelViewSet):
    queryset = File.objects.all().order_by('id')
    serializer_class = FileSerializer

    @staticmethod
    def list(request):
        files = File.objects.all().order_by('id')
        response = FileSerializer(files, many=True).data
        return Response(response)

    @staticmethod
    def create(request):
        print(request.FILES)
        print(request.data)
        name = request.data['name']
        file = request.data['file']
        if len(name) > 3 and file is not None:
            File.objects.create(name=name, file=file)
        files = File.objects.all().order_by('id')
        response = FileSerializer(files, many=True).data
        return Response(response)

    @action(methods=['get'], detail=True)
    def parse_file(self, request, pk):
        print(pk)
        selected_file = FileSerializer(File.objects.get(id=pk)).data
        print(selected_file['file'])
        es = ExpertSystem
        response = es.open_file(es, selected_file['file'])

        return Response(response)
