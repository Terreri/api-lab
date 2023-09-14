from rest_framework import serializers
from .models import User, Lab

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'is_active', 'cpf_cnpj', 'phone','user_type']
        
class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields = ['id', 'floor', 'lab', 'description', 'is_active']