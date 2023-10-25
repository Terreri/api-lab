from rest_framework import serializers
from .models import User, Lab, Payment, Reservation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password',
                  'is_active', 'cpf_cnpj', 'phone', 'user_type']


class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields = ['id', 'floor', 'lab', 'description', 'is_active']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'boleto', 'payment_date', 'status', 'user_id']


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'reservation_date', 'user', 'lab', 'payment', 'is_active']
