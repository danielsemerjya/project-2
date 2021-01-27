from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class User(AbstractUser):
    pass
def __str__(self):
        return f"{self.username}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=240)
    img = models.ImageField(null=True, blank=True, upload_to="images/")
    category = models.CharField(max_length=64)
    status = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.title}, in category {self.category}"

class Watch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_name")
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE,related_name = "list", blank=True, default=None)
    def __str__(self):
        return f"{self.auction}, by user {self.user}"

class Bid(models.Model):
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    price = models.DecimalField(max_digits=19, decimal_places=2, blank=False, validators=[MinValueValidator(1)])
    class Meta:
        get_latest_by = 'price'
    def __str__(self):
        return f"{self.listing_id.title} bid as {self.price}"

class Comment(models.Model):
    time = models.DateTimeField(auto_now=True, auto_now_add=False)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comment")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")
    text = models.CharField(max_length=240, blank=False)