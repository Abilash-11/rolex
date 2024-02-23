from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# class UserType(models.Model):
#     name = models.CharField(max_length=30)
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
#     created_by = models.DateTimeField(auto_now_add=True)
#     modified_by = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name

class UserType(models.Model):
    name = models.CharField(max_length=30)
    created_by = models.DateTimeField(auto_now_add=True)
    modified_by = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Access(models.Model):
    user_map = models.ForeignKey(User,on_delete=models.CASCADE)
    user_type_map = models.ForeignKey(UserType,on_delete=models.CASCADE)


class Size(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Product_type(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class genter(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Prand(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.ForeignKey(Prand,on_delete=models.CASCADE,null = True)
    genter = models.ForeignKey(genter,on_delete=models.CASCADE)
    product_type = models.ForeignKey(Product_type,on_delete=models.CASCADE)
    size = models.ForeignKey(Size,on_delete=models.CASCADE)
    count = models.PositiveIntegerField()
    mrp = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()



class SaleProduct(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    size = models.ForeignKey(Size,on_delete=models.CASCADE)
    count = models.PositiveIntegerField()
    mrp = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()
    status = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.Product.name


class Payment(models.Model):
    cash = models.PositiveIntegerField(default=0)
    upi = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.id

class TotalSale(models.Model):
    customer_name = models.CharField(max_length=30,null=True)
    ph_no = models.CharField(max_length=30,null=True)
    date = models.DateField(auto_now_add=True)
    total_amount = models.PositiveIntegerField()
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE)
    product = models.ManyToManyField(SaleProduct)

    def __str__(self):
        return self.customer_name
    
class UserType(models.Model):
    name = models.CharField(max_length=30)
    created_by = models.DateTimeField(auto_now_add=True)
    modified_by = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Access(models.Model):
    user_map = models.ForeignKey(User,on_delete=models.CASCADE)
    user_type_map = models.ForeignKey(UserType,on_delete=models.CASCADE)

class stackProduct(models.Model):
    name = models.ForeignKey(Product,on_delete=models.CASCADE,null = True)
    count = models.PositiveIntegerField()
    mrp = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()
    created_by = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class finalbill(models.Model):
    name = models.CharField(max_length=50)
    count = models.PositiveIntegerField()
    mrp = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    status = models.BooleanField(default=False)