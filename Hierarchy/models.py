from django.db import models
from django.core.validators import validate_comma_separated_integer_list

class Person(models.Model):
	first_name= models.CharField(max_length = 100)
	surname_name= models.CharField(max_length = 100)
	age = models.IntegerField()
	personal_id = models.AutoField(primary_key = True)
	position = models.CharField(max_length = 200)
	tasks_ids = models.CharField(validators=[validate_comma_separated_integer_list],max_length=200, default="")
	#subordinates_id = models.ListIntegerField()

	def __str__(self):
		return self.first_name + " " + self.surname_name + " (" + self.position + ")"


# Create your models here.
