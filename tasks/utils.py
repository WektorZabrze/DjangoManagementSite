import datetime


def calculate_productivity_index(task):
    if task.priority == 'LOW':
        ratio = 0.6
    elif task.priority == 'HIG':
        ratio = 1.4
    elif task.priority == 'CRI':
        ratio = 1.8
    else:
        ratio = 1.0

    numerator = (task.deadline_date.date() - task.end_date.date()).total_seconds()*ratio

    denominator = (task.deadline_date.date() - task.created_date.date()).total_seconds()

    if denominator == 0:
        return 0
    return float("{0:.2f}".format(numerator/denominator))

