from django.db import models

class UserType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_type'

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=False)
    email = models.CharField(max_length=255, unique=True, blank=True, null=False)
    password = models.CharField(max_length=255, blank=True, null=False)
    is_active = models.BooleanField(blank=True, null=False)
    cpf_cnpj = models.CharField(max_length=14, unique=True, blank=True, null=False)
    phone = models.CharField(max_length=20, blank=True, null=False)
    user_type = models.ForeignKey(UserType, on_delete=models.DO_NOTHING, blank=True, null=False)

    class Meta:
        managed = False
        db_table = 'users'
        
class Lab(models.Model):
    id = models.AutoField(primary_key=True)
    floor = models.IntegerField(blank=True, null=False)
    lab = models.CharField(max_length=255, unique=True, blank=True, null=False)
    description = models.CharField(max_length=500, unique=True, blank=True, null=False)
    is_active = models.BooleanField(blank=True, null=False)

    class Meta:
        managed = False
        db_table = 'labs'