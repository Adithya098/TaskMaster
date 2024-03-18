from taskmaster import app, Task
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from tabulate import tabulate
import warnings
import sqlalchemy.exc


warnings.filterwarnings('ignore', category=sqlalchemy.exc.SAWarning)

# Create an application context
with app.app_context():
    tasks = Task.query.all()  # Query all tasks
    # Define table headers including 'Task Description' and 'Task Progress'
    table = [["Task Id", "Task Name", "Task Description", "Task Deadline", "Task Priority", "Task Progress", "User ID"]]  
    # Extend table with rows containing task details including description and progress
    for task in tasks:
        table.append([task.id, task.name, task.description, task.deadline, task.priority, task.progress, task.user_id])

    # Print the table using tabulate with reduced column width
    print(tabulate(table, headers="firstrow", tablefmt="grid", numalign="left", stralign="left"))

