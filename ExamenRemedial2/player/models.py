from django.db import models

from django.db import models
from team.models import Team

class Player(models.Model):
	name = models.CharField(max_length=100)
	number = models.PositiveIntegerField()
	position = models.CharField(max_length=50)
	team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')

	def __str__(self):
		return f"{self.name} ({self.number})"
