from task import Task

import json

def save_tasks(tasks):
    task_list = [{"title": task.title, "priority": task.priority, "status": task.status, "task_id": task.task_id} for task in tasks]
    with open("tasks.json", "w") as f:
        json.dump(task_list, f)
def load_tasks():
    with open("tasks.json", "r") as f:
        loaded = json.load(f)
    return [Task(d["title"], d["priority"], d["status"], d["task_id"]) for d in loaded]
