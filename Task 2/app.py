from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'task2intern'  # Change this in production
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    projects = db.relationship('Project', backref='user', lazy=True)
    skills = db.relationship('Skill', backref='user', lazy=True)
    experiences = db.relationship('Experience', backref='user', lazy=True)
    educations = db.relationship('Education', backref='user', lazy=True)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    proficiency = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(120), nullable=False)
    position = db.Column(db.String(120), nullable=False)
    start_date = db.Column(db.String(80), nullable=False)
    end_date = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    institution = db.Column(db.String(120), nullable=False)
    degree = db.Column(db.String(120), nullable=False)
    field_of_study = db.Column(db.String(120))
    start_date = db.Column(db.String(80), nullable=False)
    end_date = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

with app.app_context():
    db.create_all()

# Authentication Routes
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password required'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200

# Project Routes
@app.route('/api/projects', methods=['GET'])
@jwt_required()
def get_projects():
    current_user_id = get_jwt_identity()
    projects = Project.query.filter_by(user_id=current_user_id).all()
    return jsonify([{
        'id': project.id,
        'title': project.title,
        'description': project.description
    } for project in projects]), 200

@app.route('/api/projects', methods=['POST'])
@jwt_required()
def create_project():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data.get('title') or not data.get('description'):
        return jsonify({'message': 'Title and description required'}), 400

    new_project = Project(
        title=data['title'],
        description=data['description'],
        user_id=current_user_id
    )
    db.session.add(new_project)
    db.session.commit()
    return jsonify({'message': 'Project created', 'id': new_project.id}), 201

@app.route('/api/projects/<int:project_id>', methods=['PUT', 'DELETE'])
@jwt_required()
def manage_project(project_id):
    current_user_id = get_jwt_identity()
    project = Project.query.get_or_404(project_id)

    if project.user_id != current_user_id:
        return jsonify({'message': 'Unauthorized'}), 403

    if request.method == 'PUT':
        data = request.get_json()
        project.title = data.get('title', project.title)
        project.description = data.get('description', project.description)
        db.session.commit()
        return jsonify({'message': 'Project updated'}), 200

    if request.method == 'DELETE':
        db.session.delete(project)
        db.session.commit()
        return jsonify({'message': 'Project deleted'}), 200

# Similar routes for Skills, Experiences, and Educations would follow the same pattern

if __name__ == '__main__':
    app.run(debug=True)
