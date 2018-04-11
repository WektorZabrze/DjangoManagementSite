from django.db import models
from django.core.validators import validate_comma_separated_integer_list

class Person(models.Model):
	first_name= models.CharField(max_length = 100)
	surname= models.CharField(max_length = 100)
	age = models.IntegerField()
	personal_id = models.AutoField(primary_key = True)
	position = models.CharField(max_length = 200)
	task_ids = models.CharField(validators=[validate_comma_separated_integer_list],max_length=200, default="", editable=False)
	subordinate_ids =  models.CharField(validators=[validate_comma_separated_integer_list],max_length=200, default="", editable=False)

	def __str__(self):
		return self.first_name + " " + self.surname + " (" + self.position + " " + str(self.personal_id) + ")"

	def turn_on_edit(self):
		task_ids.editable=True
		subordinate_ids.editable=True
		
# Create your models here.
