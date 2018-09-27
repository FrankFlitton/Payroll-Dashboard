from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView

import csv

# Create your views here.
@api_view(['POST'])
@parser_classes((MultiPartParser,))
def csv_reader_view(request, format=None):
    f = open(
        request.FILES["file"],
        'rb'
    )
    reader = csv.reader(f)
    for row in reader:
        print row
    f.close()

    return Response(
        status=204,
        {'received data': request.data}
    )
