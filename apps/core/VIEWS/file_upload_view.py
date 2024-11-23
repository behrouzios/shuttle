from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from apps.core.API.serializers import FileUploadSerializer
import csv
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class FileUploadAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file_instance = serializer.save(user=request.user)
            extracted_data = []
            try:
                with open(file_instance.file.path, 'r') as csv_file:
                    reader = csv.DictReader(csv_file)
                    extracted_data = [row for row in reader]
            except Exception as e:
                return Response({"message": "Error reading CSV file", "error": str(e)},
                                status=status.HTTP_400_BAD_REQUEST)

            return Response(
                {"message": "File uploaded successfully", "data": extracted_data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
