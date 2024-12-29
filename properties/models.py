from django.db import models
from django.utils.timezone import now
from django.contrib.auth import get_user_model
User= get_user_model()

# Create your models here.

class properties(models.Model):

    class SaleType(models.TextChoices):
        FOR_SALE = 'For Sale',
        FOR_RENT = 'For Rent',
        FOR_LEASE = 'For Lease',
    
    class HomeType(models.TextChoices):
       HOUSE = 'House',
       APARTMENT = 'Apartment',
       TOWNHOUSE = 'Townhouse',
       CONDO = 'Condo',
       


    agent = models.EmailField(max_length=255)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=20)
    description = models.TextField()
    price = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.DecimalField(max_digits = 2 ,decimal_places = 1)
    sale_type = models.CharField(max_length=255, choices=SaleType.choices,default = SaleType.FOR_SALE)
    home_type = models.CharField(max_length=255, choices=HomeType.choices,default = HomeType.HOUSE)
    main_image = models.ImageField(upload_to='properties/')
    image_1 = models.ImageField(upload_to='properties/')
    image_2 = models.ImageField(upload_to='properties/')
    image_3= models.ImageField(upload_to='properties/')
    is_published = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=now)

    def __str__(self):
        return self.title
    

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="client_profile")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    favorite_properties = models.ManyToManyField(properties, blank=True, related_name="favorited_by")

    def __str__(self):
        return self.user.name
    
class Inquiry(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="inquiries")
    property = models.ForeignKey(properties, on_delete=models.CASCADE, related_name="inquiries")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry by {self.client.user.name} for {self.property.title}"

class Interaction(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="interactions")
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interaction with {self.client.user.name} on {self.timestamp}"
    

class Appointment(models.Model):
    # STATUS_CHOICES = [
    #     ('Pending', 'Pending'),
    #     ('Approved', 'Approved'),
    #     ('Rescheduled', 'Rescheduled'),
    #     ('Cancelled', 'Cancelled'),
    # ]
    class StatusType(models.TextChoices):
       PENDING = 'Pending',
       APPROVED = 'Approved',
       RESCHEDULED = 'Rescheduled',
       CANCELLED = 'Cancelled',

    property = models.ForeignKey(properties, on_delete=models.CASCADE, related_name='appointments')
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    client_phone = models.CharField(max_length=15)
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    status = models.CharField(max_length=20, choices=StatusType.choices,default = StatusType.PENDING)
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.client_name} - {self.property.title}"

class Contract(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    images = models.ImageField(upload_to='properties/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title