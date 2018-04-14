from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_comma_separated_integer_list

class Person(AbstractUser):
	first_name = models.CharField(max_length = 100, default = "")
	surname = models.CharField(max_length = 100, default = "")
	date_of_birth = models.DateField(default = "1900-01-01")
	personal_id = models.AutoField(primary_key = True)
	subordinate_ids = models.CharField(validators = [validate_comma_separated_integer_list], max_length = 200, default = "") 
	is_admin = models.BooleanField(default = False)
	position = models.CharField(max_length = 3, choices =(
		('BOS', 'Boss'),
		('MAN', 'Manager'),
		('SUP', 'Supervisor'),
		('WOR', 'Worker'),
		), default = 'WOR',
	)

# Create your models here.
