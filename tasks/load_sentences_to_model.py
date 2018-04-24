from .models import Task
from users.models import Person
import csv

#it's used to download tasks from file to model!

def loading():
    with open("tasks/text_dimensionality_reduction/snli_1.0_dev.csv", newline='') as csvFile:
        rowNumber = 0
        reader = csv.reader(csvFile, delimiter=',')
        for row in reader:
            # check if row isnt empty
            if len(row) != 0:
                currentSentence = row[6]  # number of column from which we want to extract text
                print(currentSentence)

                created = Task.objects.get_or_create(
                    task_name = currentSentence,
                    assigned_employee = Person.objects.get(first_name = "aaaaaaaa"),
                )
                rowNumber += 1
                if rowNumber == 1:
                    break