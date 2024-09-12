from pymongo import MongoClient
from pymongo.errors import OperationFailure

conn = MongoClient()

conn.local.user.create_index("email", unique=True)
conn.local.project.create_index("project_code", unique=True)
conn.local.task.create_index("task_name", unique=True)


