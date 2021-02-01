from django.db import models
from django.contrib.auth.models import User

# models for server
class BotServer(models.Model):
    server_name = models.CharField(max_length=50)
    server_id = models.IntegerField()
    enc_key = models.TextField(default="TEST")

    def __str__(self):
        return self.server_name

# Model to collect sheduling data to deploy algos to the arena
class Schedule(models.Model):
    project_name = models.CharField(max_length=100)
    description = models.TextField()
    server_id = models.ForeignKey(BotServer, default=None, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.project_name
