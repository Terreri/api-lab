from django.contrib import admin
from django.urls import path
from rest_framework import routers
from lab_app.views import UserView ,UserViewSet, LabViewSet, LoginUserView, RegisterUserView, ReservationViewSet, PaymentViewSet, RegisterPaymentView, RegisterReservationView, LabView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

"""
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'labs', LabViewSet)
router.register(r'payment', PaymentViewSet)
router.register(r'reservation', ReservationViewSet)
"""

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('user/<int:id>', UserView.as_view(), name='user'),
    path('reservation/<int:user_id>', RegisterReservationView.as_view(), name='reservation'),
    path('pay/', RegisterPaymentView.as_view(), name='pay'), 
    path('lab/', LabView.as_view(), name='lab'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

#urlpatterns += router.urls