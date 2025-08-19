from django.db import models

from django.db import models

class Stadium(models.Model):
	name = models.CharField(max_length=100)
	capacity = models.PositiveIntegerField()
	box_size = models.CharField(max_length=50)

	def __str__(self):
		return self.name
