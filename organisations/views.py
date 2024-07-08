from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from users.models import User
from .models import Organisation
from .serializers import OrganisationSerializer, CreateOrganisationSerializer, AddUserToOrganisationSerializer
from .services import OrganisationService


class OrganisationListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrganisationSerializer

    def get_queryset(self):
        return Organisation.objects.filter(users=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = CreateOrganisationSerializer(data=request.data)
        if not serializer.is_valid():
            errors = [
                {"field": field, "message": str(error[0])}
                for field, error in serializer.errors.items()
            ]
            return Response(
                {"errors": errors},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        try:
            payload = serializer.validated_data
            data = OrganisationService.create_organisation(payload, request.user)
            serializer = OrganisationSerializer(data)
            return Response(
                {
                    "status": "success",
                    "message": "Organisation created successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {
                    "status": "Bad Request",
                    "message": "Client Error",
                    "statusCode": 400
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "status": "success",
                "message": "Organisations fetched successfully",
                "data": {"organisations": serializer.data}
            },
            status=status.HTTP_200_OK
        )


class OrganisationDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrganisationSerializer
    lookup_field = 'orgId'

    def get_queryset(self):
        return Organisation.objects.filter(users=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {
                "status": "success",
                "message": "Organisation details fetched successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


class AddUserToOrganisationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, orgId, *args, **kwargs):
        # Get the organisation
        organisation = get_object_or_404(Organisation, orgId=orgId)

        # Validate the request data
        serializer = AddUserToOrganisationSerializer(data=request.data)
        if not serializer.is_valid():
            errors = [
                {"field": field, "message": str(error[0])}
                for field, error in serializer.errors.items()
            ]
            return Response(
                {"errors": errors},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        # Get the user to be added
        user_id = request.data.get("userId")
        user = get_object_or_404(User, userId=user_id)

        try:
            # Add the user to the organisation
            organisation.users.add(user)
            return Response(
                {
                    "status": "success",
                    "message": "User added to organisation successfully"
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    "status": "fail",
                    "message": str(e),
                    "statusCode": 400
                },
                status=status.HTTP_400_BAD_REQUEST
            )
