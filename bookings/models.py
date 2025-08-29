from django.db import models
from django.contrib.auth.models import User
from travels.models import TravelOption

# Create your models here.
class Booking(models.Model):
    choices = [
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled')
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    travel_option = models.ForeignKey(TravelOption,on_delete=models.CASCADE)
    number_of_seats = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=100,choices=choices)