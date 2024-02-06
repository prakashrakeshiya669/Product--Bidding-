from django.db import models

class Register(models.Model):
    regid=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=50, unique=True)
    password=models.CharField(max_length=18)
    mobile=models.CharField(max_length=12)
    address=models.CharField(max_length=300)
    city=models.CharField(max_length=40)
    gender=models.CharField(max_length=20)
    status=models.IntegerField()
    role=models.CharField(max_length=20)
    info=models.CharField(max_length=20)

