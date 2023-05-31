from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Subscription(models.Model):
    user = models.ForeignKey(
        User, related_name='follower', null=False, on_delete=models.CASCADE)
    author = models.ForeignKey(User,
                               null=False, related_name='followed_user',
                               on_delete=models.CASCADE)
