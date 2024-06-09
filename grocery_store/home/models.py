from django.db import models
from django.core.exceptions import ValidationError

class Admin(models.Model):
    Admin_Name = models.CharField(primary_key = True, max_length=50)
    password = models.CharField(max_length=50)

    class Meta:
        db_table = 'admin'

class Order(models.Model):
    ID = models.AutoField(primary_key=True)
    OrderID = models.IntegerField()
    ItemID = models.IntegerField()
    Quantity = models.IntegerField()
    price = models.FloatField()
    OrderDate = models.DateTimeField(null=True, blank=True)
    Mode_of_payment = models.CharField(max_length=50)
    Trip_Status = models.IntegerField()
    CustomerID = models.IntegerField()
    PartnerID = models.IntegerField()
    VendorID = models.IntegerField()
    CategoryID = models.IntegerField()

    class Meta:
        db_table = 'order'

class DeliveryBoy(models.Model):
    BoyID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50)
    Vehicle = models.CharField(max_length=50)
    PhoneNumber = models.IntegerField()

    class Meta:
        db_table = 'deliveryboy'
        
class Offers(models.Model):
    PromoCode = models.CharField(primary_key=True, max_length=50)
    Percentage = models.IntegerField()
    MinOrderValue = models.IntegerField()

    class Meta:
        db_table = 'offer'
        

class Category(models.Model):
    CategoryID = models.AutoField(primary_key=True)
    Category_Name = models.CharField(max_length=50, default='default_name')

    class Meta:
        db_table = 'category'

class Item(models.Model):
    ProductID = models.AutoField(primary_key=True)
    Name_of_the_item = models.CharField(max_length=50)
    Quantity = models.IntegerField()
    Description = models.CharField(max_length=50)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    CategoryID = models.ForeignKey('Category', on_delete=models.CASCADE)

    class Meta:
        db_table = 'item'

    # def clean(self):
    #     if self.Quantity < 0:
    #         raise ValidationError('Quantity must be a non-negative integer.')
    #     if self.Price < 0:
    #         raise ValidationError('Price must be a non-negative decimal number.')

    # def save(self, *args, **kwargs):
    #     self.clean()
    #     super(Item, self).save(*args, **kwargs)



class Vendor(models.Model):
    VendorID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50)
    PhoneNumber = models.IntegerField()
    Address = models.CharField(max_length=50)

    class Meta:
        db_table = 'vendor'
