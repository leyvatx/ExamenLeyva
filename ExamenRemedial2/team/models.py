from django.db import models
from owner.models import Owner

from django.db import models

class Team(models.Model):
	name = models.CharField(max_length=100)
	venue = models.CharField(max_length=100)
	owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='teams')

	def __str__(self):
		return self.name
