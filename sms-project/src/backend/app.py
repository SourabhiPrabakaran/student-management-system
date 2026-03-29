"""
Student Management System - Backend API
Course: ISWE403L - Software Configuration Management
"""

from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
import mysql.connector
import hashlib
import os

app = Flask(__name__, static_folder='../../frontend', static_url_path='')
app.secret_key = 'scm-demo-secret-2026'
CORS(app)

# ─── Database Configuration ───────────────────────────────────────────────────
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'password'),
    'database': os.environ.get('DB_NAME', 'sms_db')
}


def get_db():
    """Create and return a database connection."""
    return mysql.connector.connect(**DB_CONFIG)


def hash_password(password):
    """Hash password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


# ─── Static File Routes ───────────────────────────────────────────────────────
@app.route('/')
def index():
    return send_from_directory('../../frontend', 'login.html')


@app.route('/dashboard')
def dashboard():
    return send_from_directory('../../frontend', 'dashboard.html')


@app.route('/students-page')
def students_page():
    return send_from_directory('../../frontend', 'students.html')


# ─── Auth Routes ──────────────────────────────────────────────────────────────
@app.route('/api/login', methods=['POST'])
def login():
    """Authenticate user and create session."""
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')

    if not username or not password:
        return jsonify({'success': False, 'message': 'Username and password required'}), 400

    # For demo: hardcoded admin user (in production, use DB)
    if username == 'admin' and password == 'admin123':
        session['user'] = username
        session['role'] = 'admin'
        return jsonify({'success': True, 'message': 'Login successful', 'role': 'admin'})

    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401


@app.route('/api/logout', methods=['POST'])
def logout():
    """Clear user session."""
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out'})


# ─── Student Routes ───────────────────────────────────────────────────────────
@app.route('/api/students', methods=['GET'])
def get_students():
    """Return list of all students."""
    # Demo data (use DB in production)
    students = [
        {'id': 1, 'reg_no': 'VIT2024001', 'name': 'Arjun Kumar',
         'email': 'arjun.k@vit.ac.in', 'course': 'M.Tech SE', 'year': 1, 'cgpa': 8.7},
        {'id': 2, 'reg_no': 'VIT2024002', 'name': 'Priya Sharma',
         'email': 'priya.s@vit.ac.in', 'course': 'M.Tech SE', 'year': 1, 'cgpa': 9.1},
        {'id': 3, 'reg_no': 'VIT2024003', 'name': 'Rahul Verma',
         'email': 'rahul.v@vit.ac.in', 'course': 'M.Tech SE', 'year': 2, 'cgpa': 7.8},
        {'id': 4, 'reg_no': 'VIT2024004', 'name': 'Sneha Patel',
         'email': 'sneha.p@vit.ac.in', 'course': 'M.Tech SE', 'year': 1, 'cgpa': 8.3},
        {'id': 5, 'reg_no': 'VIT2024005', 'name': 'Karthik Rajan',
         'email': 'karthik.r@vit.ac.in', 'course': 'M.Tech SE', 'year': 2, 'cgpa': 9.4},
    ]
    return jsonify({'success': True, 'data': students, 'count': len(students)})


@app.route('/api/students', methods=['POST'])
def add_student():
    """Add a new student record."""
    data = request.get_json()
feature/update-dashboard-title
   

# Validate registration number must start with VIT
if data.get('reg_no') and not data.get('reg_no', '').startswith('VIT'):
    return jsonify({'success': False, 'message': 'Registration number must start with VIT'}), 400

required = ['reg_no', 'name', 'email', 'course']

    # Validate registration number must start with VIT
    if data.get('reg_no') and not data.get('reg_no', '').startswith('VIT'):
        return jsonify({'success': False, 'message': 'Registration number must start with VIT'}), 400
    # Validate registration number format (must start with VIT)
    reg_no = data.get('reg_no', '')
    if reg_no and not reg_no.startswith('VIT'):
        return jsonify({'success': False, 'message': 'Registration number must start with VIT'}), 400
 main
    required = ['reg_no', 'name', 'email', 'course']
    for field in required:
        if not data.get(field):
            return jsonify({'success': False, 'message': f'{field} is required'}), 400

    # In production: INSERT INTO students table
    new_student = {
        'id': 6,
        'reg_no': data['reg_no'],
        'name': data['name'],
        'email': data['email'],
        'course': data['course'],
        'year': data.get('year', 1),
        'cgpa': data.get('cgpa', 0.0)
    }
    return jsonify({'success': True, 'message': 'Student added successfully', 'data': new_student}), 201


@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """Delete a student record by ID."""
    # In production: DELETE FROM students WHERE id = student_id
    return jsonify({'success': True, 'message': f'Student {student_id} deleted'})


# ─── Course Routes ────────────────────────────────────────────────────────────
@app.route('/api/courses', methods=['GET'])
def get_courses():
    """Return list of all courses."""
    courses = [
        {'id': 1, 'code': 'ISWE401L', 'name': 'Software Architecture', 'credits': 4, 'faculty': 'Dr. Ramesh'},
        {'id': 2, 'code': 'ISWE402L', 'name': 'Advanced Algorithms', 'credits': 3, 'faculty': 'Dr. Meena'},
        {'id': 3, 'code': 'ISWE403L', 'name': 'Software Configuration Management', 'credits': 3, 'faculty': 'Dr. Suresh'},
        {'id': 4, 'code': 'ISWE404L', 'name': 'Cloud Computing', 'credits': 4, 'faculty': 'Dr. Anita'},
    ]
    return jsonify({'success': True, 'data': courses, 'count': len(courses)})


# ─── Dashboard Stats ──────────────────────────────────────────────────────────
@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Return dashboard statistics."""
    stats = {
        'total_students': 5,
        'total_courses': 4,
        'total_faculty': 12,
        'avg_cgpa': 8.66,
        'recent_changes': [
            {'type': 'feat', 'message': 'Add student registration module', 'author': 'Arjun', 'time': '2h ago'},
            {'type': 'fix', 'message': 'Fix login session timeout bug', 'author': 'Priya', 'time': '5h ago'},
            {'type': 'docs', 'message': 'Update API documentation', 'author': 'Rahul', 'time': '1d ago'},
        ]
    }
    return jsonify({'success': True, 'data': stats})


# ─── Health Check ─────────────────────────────────────────────────────────────
@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint for CI/CD."""
    return jsonify({'status': 'ok', 'version': '1.0.0', 'app': 'Student Management System'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
