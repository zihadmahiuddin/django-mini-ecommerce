from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    image_url = models.URLField()
    price = models.FloatField()
    stock = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.name} by {self.owner.username}"


class Cart(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product)


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING"
        DELIVERING = "DELIVERING"
        CONFIRMED = "CONFIRMED"

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product)
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING)
