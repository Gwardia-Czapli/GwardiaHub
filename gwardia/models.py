from django.db import models
from django.utils import timezone


class Meeting(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    date = models.DateTimeField("Date of meeting")
    duration = models.CharField(max_length=30, default="0oO")

    def is_archival(self):
        return self.date < timezone.now()

    def __str__(self):
        return f"{self.title} - {self.description:<50}"
