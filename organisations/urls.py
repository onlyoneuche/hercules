from django.urls import path
from .views import OrganisationListView, OrganisationDetailView, AddUserToOrganisationView

urlpatterns = [
    path('organisations', OrganisationListView.as_view(), name='organisation-list'),
    path('organisations/<str:orgId>', OrganisationDetailView.as_view(), name='organisation-detail'),
    path('organisations/<str:orgId>/users', AddUserToOrganisationView.as_view(), name='add-user-to-organisation'),
]
