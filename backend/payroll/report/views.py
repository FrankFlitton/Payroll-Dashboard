from django.contrib.auth.models import User, Group
from payroll.report.models import TimeReport
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from payroll.report.serializers import UserSerializer, GroupSerializer, PayrollFileSerializer
from .models import Employee, JobGroup, TimeReport

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

            # obtain CSV file
            csv_file = request.FILES['file']
            csv_file.seek(0)
            reader = csv.DictReader(io.StringIO(csv_file.read().decode('utf-8')))

            print('**********************')
            rows = list(reader)
            reader_len = len(rows) - 1

            # Create Time Report
            time_report = rows[reader_len].get('hours worked') # 2nd col
            if len(time_report) > 0:
                try:
                    time_report_obj = TimeReport.objects.get(id=time_report)
                except TimeReport.DoesNotExist:
                    time_report_obj = TimeReport(id=time_report)
                    time_report_obj.save()

            # Read each row
            row_counter = 0
            for row in rows:

                # Ignore last row
                row_counter = row_counter + 1

                if row_counter > reader_len:

                    # Set up variables
                    employee_id = row.get('employee id')
                    job_group = row.get('job group')
                    job_group = JobGroup.objects.get(id=job_group)

                    # Update or create
                    if len(employee_id) > 0:
                        try:
                            employee_obj = Employee.objects.get(id=employee_id)
                        except Employee.DoesNotExist:
                            employee_obj = Employee(id=employee_id, employee_id=employee_id)
                            employee_obj.save()

                    # if len(job_group) > 0:
                    #     try:
                    #         obj = JobGroup.objects.get(id=employee_id)
                    #     except JobGroup.DoesNotExist:
                    #         obj = JobGroup(id=employee_id, employee_id=employee_id)
                    #         obj.save()

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
