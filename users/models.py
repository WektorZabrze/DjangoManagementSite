from django.db import models
from django.contrib.auth.models import AbstractUser


class Person(AbstractUser):
    first_name = models.CharField(max_length=100, default="")
    surname = models.CharField(max_length=100, default="")
    date_of_birth = models.DateField(default="1900-01-01")
    personal_id = models.AutoField(primary_key=True)
    subordinates = models.ManyToManyField("Person", blank=True)
    is_admin = models.BooleanField(default=False)
    position = models.CharField(max_length=3, choices=(
        ('BOS', 'Boss'),
        ('MAN', 'Manager'),
        ('SUP', 'Supervisor'),
        ('WOR', 'Worker'),
    ), default='WOR',
                                )
    productivity_index = models.FloatField(blank=True, null=True)

    def get_full_name(self):
        if self.position == "BOS":
            position = "Boss"
        elif self.position == "MAN":
            position = "Manager"
        elif self.position == "SUP":
            position = "Supervisor"
        else:
            position = "Worker"
        return self.first_name + " " + self.surname + " (" + position + ")"
