from django.db import models

class Admin(models.Model):
    AdminID = models.AutoField(primary_key=True)
    Admin_Name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    class Meta:
        db_table = 'admin'
