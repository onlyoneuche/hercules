from django.utils.crypto import get_random_string

from organisations.models import Organisation


class OrganisationService:

    @staticmethod
    def create_organisation(data, req_user):
        name = data['name']
        description = data['description']

        random_id = get_random_string(length=32)
        while Organisation.objects.filter(orgId=random_id).exists():
            random_id = get_random_string(length=32)
        org = Organisation.objects.create(name=name, orgId=random_id, description=description)
        org.users.add(req_user)
        return org
