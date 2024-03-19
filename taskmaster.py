from flask import Flask, redirect, render_template, request, session, jsonify, flash, url_for
from flask_sqlalchemy import SQLAlchemy
import warnings
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
# Define Task model
from flask_login import current_user
import sqlalchemy.exc

# Ignore all SQLAlchemy warnings
warnings.filterwarnings('ignore', category=sqlalchemy.exc.SAWarning)

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SECRET_KEY'] = '619619'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    __tablename__ = 'users'  
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    user_type = db.Column(db.String(20))  # Add this line for user type
    


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=True)
    priority = db.Column(db.Integer, nullable=False)
    deadline = db.Column(db.String(80), nullable=False)
    progress = db.Column(db.String(50), nullable=False, default="To Do")

    def __repr__(self):
        return '<Task %r>' % self.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'priority': self.priority,
            'deadline': self.deadline,
            'progress': self.progress,
        }

@app.before_request
def create_tables():
    # The following line will remove this handler, making it
    app.before_request_funcs[None].remove(create_tables)
    db.create_all()

@app.route('/')
@login_required
def index():
    # Fetch all tasks associated with the current user
    tasks = Task.query.all()
    
    # Categorize tasks by progress for the Kanban board
    todo_tasks = [task for task in tasks if task.progress == 'To Do']
    doing_tasks = [task for task in tasks if task.progress == 'In-Progress']
    done_tasks = [task for task in tasks if task.progress == 'Completed']
    
    # Pass all tasks and categorized tasks to the template
    return render_template('taskmasterpage.html', tasks=tasks, todo_tasks=todo_tasks, doing_tasks=doing_tasks, done_tasks=done_tasks)


@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    new_task = Task(
        name=data['name'],
        description=data.get('description', ''),
        priority=data['priority'],
        deadline=data['deadline'],
        progress=data.get('progress', 'To Do')
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201


@app.route('/tasks', methods=['GET'])
@login_required
def get_tasks():
    # Fetch all tasks
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

@app.route('/tasks/<int:id>', methods=['GET'])
@login_required
def get_task(id):
    # Fetch a specific task by id
    task = Task.query.get_or_404(id)
    return jsonify(task.to_dict())


@app.route('/tasks/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    task = Task.query.get(task_id)
    if task:
        data = request.get_json()
        task.name = data.get('name', task.name)
        task.description = data.get('description', task.description)
        task.priority = data.get('priority', task.priority)
        task.deadline = data.get('deadline', task.deadline)
        task.progress = data.get('progress', task.progress)
        db.session.commit()
        return jsonify(task.to_dict()), 200
    else:
        return jsonify({'message': 'Task not found'}), 404



@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted'}), 200
    else:
        return jsonify({'message': 'Task not found'}), 404

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user is None:
            flash('No account found with this email. Please sign up.', 'danger')
            return redirect(url_for('login'))
        if not check_password_hash(user.password, password):
            flash('Incorrect password. Please try again.', 'danger')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('loginpage.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        user_type = request.form.get('userType')  # Get the user type from the form
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email address already registered. Please login.', 'warning')
            return redirect(url_for('login'))
        
        if not username or not email or not password:
            flash('Missing username, email, or password.', 'warning')
            return redirect(url_for('signup'))
        
        hashed_password = generate_password_hash(password)
        user = User(username=username, email=email, password=hashed_password, user_type=user_type)  # Add user_type to the User object
        db.session.add(user)
        db.session.commit()
        
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signuppage.html')

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  
    app.run(host='0.0.0.0', port=8000, debug=True)