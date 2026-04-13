class Task:
    VALID_PRIORITIES = ["Urgent", "Important", "Necessary", ""]

    
    def __init__(self, title, priority, status, task_id):
        if priority not in Task.VALID_PRIORITIES:
            raise ValueError(f"Invalid priority: {priority}")
        self.title = title
        self.priority = priority
        self.status = status # e.g. "Open" / "Done"
        self.task_id = task_id
    