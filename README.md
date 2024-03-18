Task Master is a web application for task management.
I have created the front end using HTML, CSS, and JavaScript, and the back end with a Flask framework using Python. For data storage, I have used SQLite database.

These are the folders,files and their short description
root/
├── .vscode/
├── __pycache__/
├── instance/
├── static/
│   ├── script.js             : Javascript file for handling task operations in a web application like creating, updating, deleting, and displaying tasks.
│   └── taskmasterstyles.css  : CSS file for styling a task management web application
├── templates/
│   ├── loginlayout.html    : HTML file defining the layout structure used for login-related pages.
│   ├── loginpage.html      : HTML file for displaying the user login interface.
│   ├── signuppage.html     : HTML file for displaying the user registration form.
│   └── taskmasterpage.html : HTML file for the main interface of the task management application.
├── TaskMaster_Report.pdf   : Report of the entire project
├── logindb.py              : run this Python file to see the details of the users.
├── tasksdb.py              : run this Python file to see the details of the tasks of different users.
└── taskmaster.py           : Python Flask web application provides a task management system with user authentication, allowing users to sign up, log in, create, view, update, 
                              and delete personal tasks with attributes such as name, description, priority, deadline, and progress.

