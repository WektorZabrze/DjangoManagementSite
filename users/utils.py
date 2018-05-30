from tasks.models import Task
from django.db.models import Field


def calculate_productivity_index(person_id):
    numerator = 0
    denominator = 0
    for task in Task.objects.all():
        if task.assigned_employee.personal_id == person_id and task.productivity_index is not None:
            numerator = numerator + task.productivity_index
            denominator = denominator + 1
    if denominator == 0:
        return 0
    return float("{0:.2f}".format(numerator/denominator))
