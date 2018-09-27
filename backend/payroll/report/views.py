from django.contrib.auth.models import User, Group
from payroll.report.models import TimeReport
from rest_framework import viewsets, views
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.response import Response
from payroll.report.serializers import UserSerializer, GroupSerializer


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

class ReporViewSet(views.APIView):
    parser_classes = (FileUploadParser,)
    queryset = TimeReport.objects.all()

    def put(self, request, filename, format=None):
        file_obj = request.data['file']
        print(file_obj)
        # ...
        # do some stuff with uploaded file
        # ...
        return Response(status=204)

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
