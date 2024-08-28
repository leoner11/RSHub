from django.db import models

# Create your models here.
class UserCredits(models.Model):
    current_credits = models.IntegerField(default=None)
    user_token = models.Charfield(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        # Check if this is a new instance by checking if it exists in the database
        if not self.pk and self.current_credits is None:
            # If this is a new user_token and current_credits is not provided, initialize current_credits to 0
            self.current_credits = 0
        super(UserCredits, self).save(*args, **kwargs)