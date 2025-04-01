from django.db import models


class Book(models.Model):
    class CoverType(models.TextChoices):
        HARD = "HARD", "Hardcover"
        SOFT = "SOFT", "Softcover"

    title = models.CharField(max_length=155, unique=True)
    author = models.CharField(max_length=155)
    cover = models.CharField(max_length=4, choices=CoverType.choices)
    inventory = models.PositiveIntegerField(default=1)
    daily_free = models.DecimalField(max_digits=3, decimal_places=2)

    def __str__(self):
        return f"{self.title}, daily free - {self.daily_free} USD"
