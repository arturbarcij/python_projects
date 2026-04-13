from task import Task

arrOfTasks = []

def add_task(title, priority):
    task = Task(title, priority, "open", len(arrOfTasks) + 1)
    arrOfTasks.append(task)
    
def get_task(task_id):
    for task in arrOfTasks:
        if task.task_id == task_id:
            return task
    raise ValueError(f"Task with id:{task_id} not found.")

def get_all_tasks():
    return arrOfTasks

def modify_task(task_id, title=None, priority=None, status=None):
    task = get_task(task_id)
    if title:
        task.title = title
    if priority:
        task.priority = priority
    if status:
        task.status = status
            
def delete_task(task_id):
    task = get_task(task_id)
    arrOfTasks.remove(task)