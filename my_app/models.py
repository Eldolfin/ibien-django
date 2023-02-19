from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    This model is used to store the information of the user
    The on_delete=models.CASCADE means that if the user is deleted, the profile is also deleted
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # location of the user
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Sell(models.Model):
    """
    This model is used to store the information of the item that is being sold
    This is the main model of the app
    It has a foreign key to the user profile model so that we can know who is selling the item
    """
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to='uploaded_images/', default='default.png')
    # location of the seller
    location = models.CharField(max_length=100)
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Buy(models.Model):
    """
    This model is used to store the information of the item that is being bought
    This model is not used in the app but it is here for future use
    """
    item = models.ForeignKey(Sell, on_delete=models.DO_NOTHING)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.item.name
