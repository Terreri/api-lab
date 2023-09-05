from django.db import models

class UserType(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_type'


class Users(models.Model):
    nome = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    user_type = models.ForeignKey(UserType, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'