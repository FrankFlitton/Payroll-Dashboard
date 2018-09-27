from django.contrib.auth.models import User, Group
from payroll.report.models import TimeReport
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from payroll.report.serializers import UserSerializer, GroupSerializer, PayrollFileSerializer

import pdb
import io

import csv

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class FileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = PayrollFileSerializer(data=request.data)
        if file_serializer.is_valid():
            print("file_serializer_____")
            print(file_serializer)

            csv_file = request.FILES['file']

            csv_file.seek(0)
            reader = csv.DictReader(io.StringIO(csv_file.read().decode('utf-8')))

            for row in reader:
                print(row)

            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class ReporViewSet(viewsets.ModelViewSet):
#     parser_classes = (MultiPartParser,)
#     queryset = TimeReport.objects.all()
#     serializer_class = FileUploadSerializer

#     def post(self, request, filename, format=None):
#         file_obj = request.data['file']
#         print(request)
#         print(filename)
#         # ...
#         # do some stuff with uploaded file
#         # ...
#         return Response(status=204)

    # def post(self, request, format=None):

    #     f = open(
    #         request.FILES["file"],
    #         'rb'
    #     )
    #     reader = csv.reader(f)
    #     for row in reader:
    #         print(row)
    #     f.close()

    #     return Response(status=204)
