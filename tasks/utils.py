def calculate_performance_index(task):
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

    return float("{0:.2f}".format(numerator/denominator))

