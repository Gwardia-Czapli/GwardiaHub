from django.db import models
# Create your models here.


class NextMeeting(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    date_of_meeting = models.DateTimeField("Data spotkania")

    def __str__(self):
        return self.title
