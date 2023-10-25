from .models import User, Lab, Payment, Reservation
from rest_framework import viewsets, status
from datetime import datetime
from .serializers import UserSerializer, LabSerializer, PaymentSerializer, ReservationSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from django.db.models import Q
import requests
import random
from django.core.exceptions import ObjectDoesNotExist

#Página de Cadastro
class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception="True")
        serializer.save()
        return Response(serializer.data)

#Página de Login
class LoginUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email, password=password).first()

        if user is None:
            return Response({'error': 'Credenciais inválidas'}, status=400)

        refresh = RefreshToken.for_user(user)

        user_data = UserSerializer(user).data
        user_data["access"] = str(refresh.access_token)

        return Response(user_data, status=200)

#Profile
class UserView(APIView):
    permission_classes = [IsAuthenticated]
    
    #informações pessoais cadastradas
    def get(self, request, id):
        if request.user.id != id:
            return Response({"error": "Você não tem permissão para ver essas informações."}, status=status.HTTP_403_FORBIDDEN)

        user = get_object_or_404(User, id=id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    #Editar informações pessoais
    def put(self, request, id):
        if request.user.id != id:
            return Response({"error": "Você não tem permissão para ver essas informações."}, status=status.HTTP_403_FORBIDDEN)
        
        user = get_object_or_404(User, id=id)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterReservationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        if request.user.id != user_id:
            return Response({"error": "Você não tem permissão para realizar essa ação."}, status=status.HTTP_403_FORBIDDEN)
        

        if request.user.user_type.id == 2 or request.user.user_type.id == 1:
            serializer = ReservationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        if request.user.user_type.id == 3 :
            payment_id = request.data.get('payment')
            if payment_id == None:
                return Response({"error":"Você ainda não emitiu o boleto"}, status=status.HTTP_402_PAYMENT_REQUIRED)
            try:
                payment_obj = Payment.objects.get(id=payment_id)
            except Payment.DoesNotExist:
                return Response({'error': 'Payment not found'}, status=404)
            if payment_obj.user_id.id != request.user.id:
                return Response({"error":"Esse boleto não pertence à essa reserva"}, status=status.HTTP_403_FORBIDDEN)
            if payment_obj.status != "approved":
                return Response({"error": "Você ainda não efetuou o pagamento."}, status=status.HTTP_402_PAYMENT_REQUIRED)
            else:
                serializer = ReservationSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save(is_active=1)
                serializer.save()
                return Response(serializer.data)
        
        
    

        
class RegisterPaymentView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        url = 'https://api-go-wash-efc9c9582687.herokuapp.com/api/pay-boleto'
        headers = {
            'Authorization': 'Vf9WSyYqnwxXODjiExToZCT9ByWb3FVsjr',
        }
        boleto = str(random.randint(10000000, 99999999))
        data = {
            'boleto': boleto,
            'user_id': request.user.id
        }
        response = requests.post(url, headers=headers, data=data)
        data = response.json().get('data') 
        serializer = PaymentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)    
    
#Carrosel
class LabView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        date_required = request.data.get('date_required')
        date_required = datetime.strptime(date_required, '%Y-%m-%d').date()

        if request.user.user_type.id == 3 or request.user.user_type.id == 2:
            queryset = Lab.objects.filter(is_active=1).exclude(
                Q(reservation__reservation_date=date_required) & Q(reservation__is_active=True)
            )
        else:
            queryset = Lab.objects.all()
        
        serializer = LabSerializer(queryset, many=True)
        return Response(serializer.data)

    


'''Essas views são gerais, retornam todos os dados requisitados 
sem autenticação de usuários, 
portanto, não poderão ser fornecidas para usuários comuns'''


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LabViewSet(viewsets.ModelViewSet):
    queryset = Lab.objects.all()
    serializer_class = LabSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
