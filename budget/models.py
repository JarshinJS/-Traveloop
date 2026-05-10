from django.db import models


class BudgetEntry(models.Model):
    CATEGORY_CHOICES = [
        ('transport', 'Transport'),
        ('accommodation', 'Accommodation'),
        ('food', 'Food & Dining'),
        ('activities', 'Activities'),
        ('shopping', 'Shopping'),
        ('insurance', 'Insurance'),
        ('other', 'Other'),
    ]

    trip = models.ForeignKey('trips.Trip', on_delete=models.CASCADE, related_name='budget_entries')
    stop = models.ForeignKey(
        'trips.TripStop',
        on_delete=models.SET_NULL,
        related_name='budget_entries',
        null=True,
        blank=True,
    )
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    description = models.CharField(max_length=200, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'description', 'id']

    def __str__(self):
        label = self.description or self.get_category_display()
        return f"{label} - {self.trip.name}"
