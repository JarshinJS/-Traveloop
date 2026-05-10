import uuid
from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User


class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trips')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    cover_photo = models.ImageField(upload_to='trip_covers/', blank=True, null=True)
    total_budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_public = models.BooleanField(default=False)
    share_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} by {self.user.username}"

    @property
    def duration_days(self):
        return (self.end_date - self.start_date).days + 1

    @property
    def total_estimated_cost(self):
        budget_total = self.budget_entries.aggregate(total=Sum('amount'))['total']
        if budget_total is not None:
            return budget_total
        return sum(stop.estimated_cost for stop in self.stops.all())


class TripStop(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='stops')
    city = models.ForeignKey('cities.City', on_delete=models.SET_NULL, null=True)
    arrival_date = models.DateField()
    departure_date = models.DateField()
    order = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['order', 'arrival_date']

    def __str__(self):
        city_name = self.city.name if self.city else 'Unknown'
        return f"{city_name} stop in {self.trip.name}"

    @property
    def duration_days(self):
        return (self.departure_date - self.arrival_date).days + 1

    @property
    def estimated_cost(self):
        activity_cost = sum(
            ta.activity.estimated_cost for ta in self.trip_activities.select_related('activity').all()
        )
        stay_cost = float(self.city.cost_index) * self.duration_days if self.city else 0
        return float(activity_cost) + stay_cost


class TripActivity(models.Model):
    stop = models.ForeignKey(TripStop, on_delete=models.CASCADE, related_name='trip_activities')
    activity = models.ForeignKey('activities.Activity', on_delete=models.CASCADE)
    scheduled_date = models.DateField(null=True, blank=True)
    scheduled_time = models.TimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    actual_cost = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.activity.name} at {self.stop}"


class PackingItem(models.Model):
    CATEGORY_CHOICES = [
        ('clothing', 'Clothing'),
        ('documents', 'Documents'),
        ('electronics', 'Electronics'),
        ('toiletries', 'Toiletries'),
        ('medicine', 'Medicine'),
        ('other', 'Other'),
    ]
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='packing_items')
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    is_packed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return self.name


class TripNote(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='notes')
    stop = models.ForeignKey(TripStop, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def body(self):
        return self.content

    @body.setter
    def body(self, value):
        self.content = value


class JourneyNote(TripNote):
    class Meta:
        proxy = True
        verbose_name = 'Journey note'
        verbose_name_plural = 'Journey notes'
