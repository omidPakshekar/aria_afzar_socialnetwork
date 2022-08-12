from datetime import datetime
from django.db import models

STATUS_MESSAGE = (
    ('Accept', 'Accept'),
    ('Reject', 'Reject'),
    ('Pending', 'Pending'),
)


# class Payment(models.Model):
#     date            = models.DateTimeFie