from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # location of the user
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Sell(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to='uploaded_images/', default='default.png')
    # location of the seller
    location = models.CharField(max_length=100)
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    # id = models.AutoField(primary_key=True)
    

    def __str__(self):
        return self.name


class Buy(models.Model):
    item = models.ForeignKey(Sell, on_delete=models.DO_NOTHING)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    # date at which the item was bought
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.item.name
