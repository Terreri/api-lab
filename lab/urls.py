from django.contrib import admin
from django.urls import path
from rest_framework import routers
from lab_app.views import UserViewSet, LabViewSet, LoginView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'labs', LabViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login')
]

urlpatterns += router.urls