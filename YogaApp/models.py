from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    CATEGORY_CHOICES = [
        
        (1, "Yoga Essentials"),
        (2, "Clothing"),
        (3, "Food"),
        (4, "bodycare"),
        (5, "Books"),
        (6, "Blog"),
    ]
    name = models.CharField(max_length=100)
    price = models.FloatField()
    pdetails = models.CharField(max_length=500)
    category = models.IntegerField(choices=CATEGORY_CHOICES)
    is_active = models.BooleanField(default=True)
    pimage = models.ImageField(upload_to='images', blank=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE, db_column='uid')
    pid = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='pid')
    quantity = models.IntegerField(default=1)
    
class Order(models.Model):
    order_id = models.CharField(max_length=100)
    uid = models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    pid = models.ForeignKey(Product,on_delete = models.CASCADE,db_column='pid')
    quantity = models.IntegerField(default=1)
    # razor_pay_order_id=models.CharField(max_length=100,null=True,blank=True)
    # razor_pay_payment_id=models.CharField(max_length=100,null=True,blank=True)
    # razor_pay_payment_signature=models.CharField(max_length=100,null=True,blank=True)


