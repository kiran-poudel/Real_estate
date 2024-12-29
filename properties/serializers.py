from rest_framework import serializers
from .models import properties,Client,Inquiry,Interaction,Appointment,Contract

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = properties
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    favorite_properties = PropertySerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'user', 'phone_number', 'address', 'favorite_properties']

class InquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = ['id', 'client', 'property', 'message', 'created_at']

class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = ['id', 'client', 'description', 'timestamp']

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'

