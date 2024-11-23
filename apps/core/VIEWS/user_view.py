from apps.core.API.serializers import UserRegistrationSerializer, LoginSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class RegisterUserAPIView(APIView):
    permission_classes = []
    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "email": user.email,
            "is_staff": user.is_staff
        })


class LoginAPIView(APIView):
    permission_classes = []
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                }
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
