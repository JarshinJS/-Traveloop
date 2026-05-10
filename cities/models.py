from django.db import models


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    cost_index = models.DecimalField(
        max_digits=5, decimal_places=2, default=1.0,
        help_text="Average daily cost in USD"
    )
    popularity_score = models.IntegerField(default=0)
    image = models.ImageField(upload_to='cities/', blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Cities'
        ordering = ['-popularity_score']

    def __str__(self):
        return f"{self.name}, {self.country}"
