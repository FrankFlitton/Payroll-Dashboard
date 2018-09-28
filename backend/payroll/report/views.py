import io
import datetime
import csv

from django.contrib.auth.models import Group
from payroll.report.models import TimeReport
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from payroll.report.serializers import TimeSheetSerializer, PayrollFileSerializer
from .models import Employee, JobGroup, TimeReport, TimeSheet


class TimeSheetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Time Sheets to be viewed or edited.
    """
    queryset = TimeSheet.objects.all().order_by('pay_date')
    serializer_class = TimeSheetSerializer


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

                if row_counter < reader_len:

                    # Set up variables
                    employee_id = row.get('employee id')
                    job_group = row.get('job group')
                    hours_worked = row.get('hours worked', None)
                    pay_date = row.get('date')

                    # Update or create
                    if len(employee_id) > 0:
                        try:
                            employee_obj = Employee.objects.get(id=employee_id)
                        except Employee.DoesNotExist:
                            employee_obj = Employee(id=employee_id, employee_id=employee_id)
                            employee_obj.save()

                    if len(job_group) > 0:
                        try:
                            job_group_obj = JobGroup.objects.get(id=job_group)
                        except JobGroup.DoesNotExist:
                            print('Invalid job group: ' + job_group)
                            raise ValueError('Job group does not exist.')

                    if len(pay_date) > 0:
                        pay_date_dt = datetime.datetime.strptime(pay_date, '%d/%m/%Y')
                        time_sheet_obj = TimeSheet(
                            pay_date=pay_date_dt,
                            hours_worked=hours_worked,
                            job_group=job_group_obj,
                            employee=employee_obj,
                            report=time_report_obj,
                        )
                        time_sheet_obj.save()

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
