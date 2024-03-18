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
    assigned_tasks = db.relationship('Task', backref='assigned_user', lazy=True, overlaps="assigned_user",primaryjoin="User.id == Task.user_id")


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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Define the user_id column

    # Define relationship with User model
    user = db.relationship("User", backref=db.backref("tasks", lazy=True))

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
            'user_id': self.user_id  # user_id in the dictionary representation
        }

@app.before_request
def create_tables():
    # The following line will remove this handler, making it
    # only run on the first request
    app.before_request_funcs[None].remove(create_tables)
    db.create_all()

@app.route('/')
@login_required
def index():
    # Fetch only the tasks associated with the current user
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('taskmasterpage.html', tasks=tasks)


@app.route('/tasks', methods=['POST'])
@login_required
def add_task():
    data = request.json
    task_name = data['name']
    
    # Check if a task with the same name already exists
    existing_task = Task.query.filter_by(name=task_name, user_id=current_user.id).first()
    if existing_task:
        return jsonify({'message': 'A task with this name already exists for the current user'}), 409  # HTTP 409 Conflict

    new_task = Task(
        name=task_name,
        description=data.get('description', ''),
        priority=data['priority'],
        deadline=data['deadline'],
        progress=data.get('progress', 'To Do'),  # Default progress is "To Do"
        user_id=current_user.id  # Assign the current user's ID to the task
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201


@app.route('/tasks', methods=['GET'])
@login_required
def get_tasks():
    # Fetch only the tasks associated with the current user
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return jsonify([task.to_dict() for task in tasks])

@app.route('/tasks/<int:id>', methods=['GET'])
@login_required
def get_task(id):
    task = Task.query.get_or_404(id)
    return jsonify(task.to_dict())

@app.route('/tasks/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    task = Task.query.get(task_id)
    if task:
        # Check if the task belongs to the current user
        if task.user_id == current_user.id:
            data = request.get_json()
            task.name = data['name']
            task.description = data.get('description', task.description)
            task.priority = data['priority']
            task.deadline = data['deadline']
            task.progress = data.get('progress', task.progress)
            db.session.commit()
            return jsonify(task.to_dict()), 200
        else:
            return jsonify({'message': 'You are not authorized to update this task'}), 403  # HTTP 403 Forbidden
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
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email address already registered. Please login.', 'warning')
            return redirect(url_for('login'))
        if not username or not email or not password:
            flash('Missing username, email, or password.', 'warning')
            return redirect(url_for('signup'))
        hashed_password = generate_password_hash(password)
        user = User(username=username, email=email, password=hashed_password)
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