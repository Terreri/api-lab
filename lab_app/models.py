from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.models import User


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('O campo email é obrigatório')
        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
    def get_by_natural_key(self, email):
        return self.get(email=email)

class UserType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user_type'


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=False)
    email = models.EmailField(
        max_length=255, unique=True, blank=True, null=False)
    password = models.CharField(max_length=255, blank=True, null=False)
    is_active = models.BooleanField(default=True)
    cpf_cnpj = models.CharField(
        max_length=14, unique=True, blank=True, null=False)
    phone = models.CharField(max_length=20, blank=True, null=False)
    user_type = models.ForeignKey(
        UserType, on_delete=models.DO_NOTHING, db_column='user_type', blank=True, null=False)
    last_login = models.DateTimeField('last login', blank=True, null=True)
    is_staff = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    objects = UserManager()

    class Meta:
        managed = True
        db_table = 'user'


class Lab(models.Model):
    id = models.AutoField(primary_key=True)
    floor = models.IntegerField(blank=True, null=False)
    lab = models.CharField(max_length=255, unique=True, blank=True, null=False)
    description = models.CharField(
        max_length=500, unique=False, blank=True, null=False)
    is_active = models.BooleanField(blank=True, null=False)

    class Meta:
        managed = True
        db_table = 'lab'


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    boleto = models.CharField(
        max_length=255, unique=True, blank=True, null=False)
    payment_date = models.CharField(max_length=255, blank=True, null=False)
    status = models.CharField(max_length=255, blank=True, null=False)
    user_id = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, db_column='user', blank=True, null=False)

    class Meta:
        managed = True
        db_table = 'payment'


class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    reservation_date = models.DateField()
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, db_column='user', blank=True, null=False)
    lab = models.ForeignKey(
        Lab, on_delete=models.DO_NOTHING, db_column='lab', blank=True, null=False)
    payment = models.ForeignKey(
        Payment, on_delete=models.DO_NOTHING, db_column='payment', blank=True, null=False)
    is_active = models.BooleanField(blank=True, null=False)

    class Meta:
        managed = True
        db_table = 'reservation'


