from .models import User, Lab
from rest_framework import viewsets, status
from .serializers import UserSerializer, LabSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

class LabViewSet(viewsets.ModelViewSet):
    queryset = Lab.objects.all()
    serializer_class = LabSerializer
    
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email, password=password).first()

        if user is None:
            return Response({'error': 'Credenciais inválidas'}, status=400)
        
        user_data = UserSerializer(user).data
        return Response(user_data, status=200)

