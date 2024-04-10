from django.db import models


class NextMeeting(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    date_of_meeting = models.DateTimeField("Date of meeting")

    def __str__(self):
        return f"{self.title}"
