from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_comma_separated_integer_list

class Person(AbstractUser):
	first_name = models.CharField(max_length = 100, default = "")
	surname = models.CharField(max_length = 100, default = "")
	age = models.IntegerField(default=0)
	personal_id = models.AutoField(primary_key = True)
	position = models.CharField(max_length = 200, default = "")
	task_ids = models.CharField(validators = [validate_comma_separated_integer_list], max_length = 200, default = "") 
	subordinate_ids = models.CharField(validators = [validate_comma_separated_integer_list], max_length = 200, default = "") 

# Create your models here.
