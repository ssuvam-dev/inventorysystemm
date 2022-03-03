from typing import Deque
from django.db import models

# Create your models here.
class Stock(models.Model):
    Product=models.CharField(max_length=255)
    Total=models.IntegerField()
    Left=models.IntegerField()
    Cost=models.DecimalField(decimal_places=2,max_digits=18)
    Sold=models.IntegerField()

    def __str__(self):
        return self.Product
    class Meta:
        ordering=('Product',)

class Sales(models.Model):
    Date=models.CharField(max_length=100)
    Customer_name=models.CharField(max_length=255)
    Customer_phone=models.CharField(max_length=255)
    Customer_address=models.CharField(max_length=255)
    Product=models.CharField(max_length=255)
    Quantity=models.IntegerField()
    Rate=models.DecimalField(max_digits=100,decimal_places=2)
    Discount=models.DecimalField(max_digits=100,decimal_places=2)
    Total=models.DecimalField(max_digits=100,decimal_places=2)
    Paid=models.IntegerField()
    Due_left=models.DecimalField(max_digits=100,decimal_places=2)

    def __str__(self):
        return self.Product
    class Meta:
        ordering=('-Date',)

class Credit(models.Model):
    Date=models.CharField(max_length=100)
    Customer_name=models.CharField(max_length=255)
    Customer_phone=models.CharField(max_length=255)
    Customer_address=models.CharField(max_length=255)
    Product=models.CharField(max_length=255)
    Quantity=models.IntegerField()
    Rate=models.DecimalField(max_digits=100,decimal_places=2)
    Discount=models.DecimalField(max_digits=100,decimal_places=2)
    Total=models.DecimalField(max_digits=100,decimal_places=2)
    Paid=models.IntegerField()
    Due_left=models.DecimalField(max_digits=100,decimal_places=2)

    def __str__(self):
        return self.Product
    class Meta:
        ordering=('-Date',)
class Salesbill(models.Model):
    Date=models.CharField(max_length=100)
    Customer_name=models.CharField(max_length=255)
    Customer_phone=models.CharField(max_length=255)
    Customer_address=models.CharField(max_length=255)
    Paid=models.IntegerField()

    def __str__(self):
        return self.Customer_name
    class Meta:
        ordering=('-Date',)

class Salesbillitems(models.Model):
    Date=models.CharField(max_length=100)
    Customer_name=models.CharField(max_length=255)
    Customer_phone=models.CharField(max_length=255)
    Customer_address=models.CharField(max_length=255)
    Product=models.CharField(max_length=255)
    Quantity=models.IntegerField()
    Rate=models.DecimalField(max_digits=100,decimal_places=2)
    Discount=models.DecimalField(max_digits=100,decimal_places=2)
    Total=models.DecimalField(max_digits=100,decimal_places=2)
    def __str__(self):
        return self.Product
    class Meta:
        ordering=('-Date',)

class Purchasebill(models.Model):
    Date=models.CharField(max_length=100)
    Company_name=models.CharField(max_length=255)
    Pan=models.CharField(max_length=255)
    Customer_phone=models.CharField(max_length=255)
    Customer_address=models.CharField(max_length=255)
    Vat=models.DecimalField(max_digits=100,decimal_places=2)
    Paid=models.DecimalField(max_digits=100,decimal_places=2)

    def __str__(self):
        return self.Company_name
    class Meta:
        ordering=('-Date',)    

class Purchasebillitems(models.Model):

    Date=models.CharField(max_length=100)
    Company_name=models.CharField(max_length=255)
    Customer_phone=models.CharField(max_length=255)
    Customer_address=models.CharField(max_length=255)
    Product=models.CharField(max_length=255)
    Quantity=models.IntegerField()
    Rate=models.DecimalField(max_digits=100,decimal_places=2)
    Discount=models.DecimalField(max_digits=100,decimal_places=2)
    Total=models.DecimalField(max_digits=100,decimal_places=2)
    
    

    def __str__(self):
        return self.Product
    class Meta:
        ordering=('-Date',)
class Expenses(models.Model):
    Date=models.CharField(max_length=100)
    Purpose=models.CharField(max_length=255)
    Amount=models.IntegerField()

    def __str__(self):
        return self.Purpose
    class Meta:
        ordering=('-Date',)

class Saving(models.Model):
    Date=models.CharField(max_length=100)
    Bank=models.CharField(max_length=255)
    Amount=models.IntegerField()

    def __str__(self):
        return self.Bank
    class Meta:
        ordering=('-Date',)
