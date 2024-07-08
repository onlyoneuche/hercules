from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Organisation


class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ['orgId', 'name', 'description']

    def validate(self, attrs):
        instance = Organisation(**attrs)
        try:
            instance.full_clean()  # Perform full model validation including unique checks
        except ValidationError as e:
            error_messages = []
            for field, errors in e.message_dict.items():
                for error in errors:
                    error_messages.append({
                        'field': field,
                        'message': error
                    })
            raise serializers.ValidationError({'errors': error_messages})
        return attrs


class CreateOrganisationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255, required=False)
