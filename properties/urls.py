from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import ManagePropertyView,PropertyDetailView,PropertyView,SearchPropertyView,ClientManagementViewSet,AppointmentRequestView,AppointmentListView,AppointmentListView,PropertyListView,ContractManagementView,ContractManagementDetailView


router = DefaultRouter()
router.register('clients', ClientManagementViewSet, basename='client_management')


urlpatterns = [
    path('manage-property/', ManagePropertyView.as_view()),
    path('manage-property/', ManagePropertyView.as_view()),
    path('property-detail/', PropertyDetailView.as_view()),
    path('get-property/', PropertyView.as_view()),
    path('search/', SearchPropertyView.as_view()),

    path('api/', include(router.urls)),

    path('properties/', PropertyListView.as_view(), name='property-list'),
    path('appointments/request/', AppointmentRequestView.as_view(), name='appointment-request'),
    path('appointments/manage/', AppointmentListView.as_view(), name='appointment-manage'),
    path('appointments/manage/<int:pk>/', AppointmentListView.as_view(), name='appointment-update'),

    path('contracts/manage/', ContractManagementView.as_view(), name='contract-manage'),
    path('contracts/manage/<int:pk>/', ContractManagementDetailView.as_view(), name='contract-update'),
    



]
