# TaskMaster - A Task Management Web Application

**TaskMaster** is a comprehensive task management tool designed to help teams and individuals organize their work. The application allows users to create, view, update, and delete tasks, with additional features like Kanban boards, and user authentication to enhance task management and project tracking.

## Key Features

- **Task Management**: Create, view, update, and delete tasks with detailed information.
- **Kanban Board**: Visualize task statuses across different stages.
- **User Authentication**: Secure access with role-based permissions for project managers and developers.
- **Backend**: Powered by Flask and SQLAlchemy, with a SQLite database for data storage.

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Flask)
- **Database**: SQLite
- **Authentication**: Flask-Login 

## Roles and Permissions

### Manager

- **Full Control**: Managers have full access to all features within the application.
- **Task Creation**: Managers can create new tasks, specifying the title, description, due date, and status.
- **Task Editing**: Managers can edit all fields of a task, including:
  - **Title**: Modify the title of the task.
  - **Description**: Update the task's detailed description.
  - **Due Date**: Change the due date of the task.
  - **Status**: Update the task's status (e.g., "To Do," "In Progress," "Completed").
- **Task Deletion**: Managers can delete tasks when they are no longer needed.


### Employee (Developer)

- **Limited Editing**: Employees have restricted access to the task management features.
- **Task Creation**: Employees cannot create Task
- **Task Status Update**: Employees can only update the status of tasks assigned to them (e.g., changing from "To Do" to "In Progress").
- **View Tasks**: Employees can view all tasks assigned to them but cannot modify the title, description, or due date.
- **No Task Deletion**: Employees do not have permission to delete tasks.
- **Task Assignment**: Employees can see which tasks have been assigned to them by the manager but cannot reassign tasks.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/TaskMaster.git
   cd TaskMaster
   pip install -r requirements.txt
   python taskmaster.py

UI of Manager
<img width="1221" alt="image" src="https://github.com/user-attachments/assets/c8f112bd-a385-4943-8147-d27864ba3b81">

UI of Employee
<img width="1236" alt="image" src="https://github.com/user-attachments/assets/da7af35e-a115-4d11-a7ca-2b34f266e5e1">

## Watch the video 'TaskManager Execution.mp4' attached in this repo for a live demo of the application.

