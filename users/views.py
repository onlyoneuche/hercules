from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import User

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from organisations.models import Organisation
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.exceptions import ValidationError


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            org_name = f"{user.firstName}'s Organisation"
            org = Organisation.objects.create(name=org_name, orgId=f"org_{user.userId}")
            org.users.add(user)
            refresh = RefreshToken.for_user(user)
            return Response({
                "status": "success",
                "message": "Registration successful",
                "data": {
                    "accessToken": str(refresh.access_token),
                    "user": UserSerializer(user).data
                }
            }, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            errors = [{"field": field, "message": str(message[0])} for field, message in e.detail.items()]
            return Response({
                "errors": errors
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as e:
            return Response({
                "status": "Bad request",
                "message": "Registration unsuccessful",
                "statusCode": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({
                "status": "Bad request",
                "message": "Authentication failed",
                "statusCode": 401
            }, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.user
        access_token = serializer.validated_data['access']

        return Response({
            "status": "success",
            "message": "Login successful",
            "data": {
                "accessToken": str(access_token),
                "user": {
                    "userId": user.userId,
                    "firstName": user.firstName,
                    "lastName": user.lastName,
                    "email": user.email,
                    "phone": user.phone,
                }
            }
        }, status=status.HTTP_200_OK)


class UserDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'userId'
