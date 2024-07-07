from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Organisation
from .serializers import OrganisationSerializer
from users.models import User


class OrganisationListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrganisationSerializer

    def get_queryset(self):
        return Organisation.objects.filter(users=self.request.user)

    def perform_create(self, serializer):
        org = serializer.save()
        org.users.add(self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class OrganisationDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrganisationSerializer
    lookup_field = 'orgId'

    def get_queryset(self):
        return Organisation.objects.filter(users=self.request.user)


class AddUserToOrganisationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, orgId):
        try:
            org = Organisation.objects.get(orgId=orgId, users=request.user)
            user = User.objects.get(userId=request.data.get('userId'))
            org.users.add(user)
            return Response({
                "status": "success",
                "message": "User added to organisation successfully",
            })
        except Organisation.DoesNotExist:
            return Response({"error": "Organisation not found or you don't have access"}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
