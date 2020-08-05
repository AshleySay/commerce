from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField()
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.title} starting price: ${self.starting_bid}"

class Bids(models.Model): #foreignkey goes here
    bid = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bids")
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0)