from django.db import models


class Activity(models.Model):
    CATEGORY_CHOICES = [
        ('sightseeing', 'Sightseeing'),
        ('food', 'Food & Dining'),
        ('adventure', 'Adventure'),
        ('culture', 'Culture & Arts'),
        ('shopping', 'Shopping'),
        ('relaxation', 'Relaxation & Spa'),
        ('transport', 'Transport'),
        ('accommodation', 'Accommodation'),
    ]
    city = models.ForeignKey('cities.City', on_delete=models.CASCADE, related_name='activities')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    estimated_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    duration_hours = models.DecimalField(max_digits=4, decimal_places=1, default=1.0)
    image = models.ImageField(upload_to='activities/', blank=True, null=True)
    is_popular = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Activities'

    def __str__(self):
        return f"{self.name} ({self.city.name})"
