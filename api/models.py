from django.db import models
from django.contrib.auth.models import User
from mapbox_location_field.models import LocationField


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")
    profile_image = models.ImageField(
        upload_to="profile-images", blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    location = LocationField(map_attrs={"placeholder": "Pick your location"})
    bio = models.TextField(blank=True, null=True)
    USER_TYPES = (('dr', 'Driver'), ('me', 'Mechanic'))
    user_type = models.CharField(
        max_length=20, choices=USER_TYPES, default='driver')
    hourly_rate = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    telephone_number = models.CharField(max_length=15, blank=True, null=True)
    skills = models.ManyToManyField(Skill, blank=True)
    is_profile_complete = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Review(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    driver = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='driver_reviews')
    mechanic = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='mechanic_reviews')
    content = models.TextField(blank=True, null=True)
    rating = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.driver.username} reviews {self.mechanic.username}"

    def save(self, *args, **kwargs):
        if self.rating < 1 or self.rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        super().save(*args, **kwargs)


class ServiceRequest(models.Model):
    driver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='service_requests')
    description = models.TextField()
    location = models.CharField(max_length=255)
    location = LocationField(map_attrs={"placeholder": "Request location"})
    created_at = models.DateTimeField(auto_now_add=True)
    is_fulfilled = models.BooleanField(default=False)

    def __str__(self):
        return f"Request by {self.driver.username} at {self.created_at}"


class Availability(models.Model):
    mechanic = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='availabilities')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('mechanic', 'date', 'start_time', 'end_time')

    def __str__(self):
        return f"{self.mechanic.username} - {self.date} {self.start_time}-{self.end_time}"


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    estimated_duration = models.DurationField()
    average_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='vehicles')
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    vin = models.CharField(max_length=17, unique=True)

    def __str__(self):
        return f"{self.year} {self.make} {self.model} - {self.owner.username}"


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    driver = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='orders')
    mechanic = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='mechanic_orders')
    note = models.TextField()
    location = models.CharField(max_length=255)
    location = LocationField(map_attrs={"placeholder": "Service location"})
    ordered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    service_date = models.DateTimeField(null=True, blank=True)
    services = models.ManyToManyField(Service)
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.SET_NULL, null=True, related_name='orders')

    def __str__(self):
        return f"{self.driver.username} : {self.mechanic.username}"
