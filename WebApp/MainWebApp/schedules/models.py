from django.db import models

# Model to collect sheduling data to deploy algos to the arena
class Schedule(models.Model):
    project_name = models.CharField(max_length=100)
    description = models.TextField()
    server_id = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project_name
