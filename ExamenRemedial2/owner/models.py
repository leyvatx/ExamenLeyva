from django.db import models

from django.db import models
from stadium.models import Stadium

class Owner(models.Model):
	name = models.CharField(max_length=100)
	stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE, related_name='owners')

	def __str__(self):
		return self.name
