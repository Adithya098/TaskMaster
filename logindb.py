from tabulate import tabulate
from taskmaster import app, User
import warnings
import sqlalchemy.exc


warnings.filterwarnings('ignore', category=sqlalchemy.exc.SAWarning)

# Push the Flask application context
app.app_context().push()

# Query all users
users = User.query.all()

# Prepare data for tabulate
table = [["User ID", "Username", "Email", "Password"]]
for user in users:
    obscured_password = "**********" if user.password else ""
    table.append([user.id, user.username, user.email, obscured_password])

# Print user details in a table format
print(tabulate(table, headers="firstrow", tablefmt="grid"))

