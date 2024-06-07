from django.db import models

# Create your models here.

class Admin(models.Model):
    AdminID = models.AutoField(primary_key=True)
    Admin_Name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.Admin_Name
