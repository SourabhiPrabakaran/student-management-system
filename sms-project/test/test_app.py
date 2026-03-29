"""
Unit Tests for Student Management System API
Course: ISWE403L - Software Configuration Management
Configuration Item: /test/test_app.py
"""
import pytest
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'backend'))

from app import app, hash_password


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret'
    with app.test_client() as client:
        yield client


# ─── Health Check Tests ───────────────────────────────────────
class TestHealth:
    def test_health_endpoint_returns_200(self, client):
        """Health check should always return 200."""
        response = client.get('/api/health')
        assert response.status_code == 200

    def test_health_response_has_status_ok(self, client):
        """Health response should contain status: ok."""
        response = client.get('/api/health')
        data = response.get_json()
        assert data['status'] == 'ok'

    def test_health_response_has_version(self, client):
        """Health response should include a version field."""
        response = client.get('/api/health')
        data = response.get_json()
        assert 'version' in data


# ─── Authentication Tests ─────────────────────────────────────
class TestAuthentication:
    def test_login_with_valid_credentials(self, client):
        """Valid admin login should return success."""
        response = client.post('/api/login',
            json={'username': 'admin', 'password': 'admin123'},
            content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True

    def test_login_with_wrong_password(self, client):
        """Wrong password should return 401."""
        response = client.post('/api/login',
            json={'username': 'admin', 'password': 'wrongpassword'},
            content_type='application/json')
        assert response.status_code == 401
        data = response.get_json()
        assert data['success'] is False

    def test_login_with_missing_fields(self, client):
        """Missing credentials should return 400."""
        response = client.post('/api/login',
            json={'username': ''},
            content_type='application/json')
        assert response.status_code == 400

    def test_login_returns_role(self, client):
        """Successful login should return user role."""
        response = client.post('/api/login',
            json={'username': 'admin', 'password': 'admin123'},
            content_type='application/json')
        data = response.get_json()
        assert 'role' in data
        assert data['role'] == 'admin'

    def test_logout_endpoint(self, client):
        """Logout should succeed."""
        response = client.post('/api/logout')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True


# ─── Student API Tests ────────────────────────────────────────
class TestStudentsAPI:
    def test_get_students_returns_200(self, client):
        """GET /api/students should return 200."""
        response = client.get('/api/students')
        assert response.status_code == 200

    def test_get_students_returns_list(self, client):
        """GET /api/students should return a list in 'data' field."""
        response = client.get('/api/students')
        data = response.get_json()
        assert 'data' in data
        assert isinstance(data['data'], list)

    def test_get_students_count_matches_data(self, client):
        """Count field should match actual list length."""
        response = client.get('/api/students')
        data = response.get_json()
        assert data['count'] == len(data['data'])

    def test_add_student_with_valid_data(self, client):
        """POST /api/students with valid data should return 201."""
        response = client.post('/api/students',
            json={
                'reg_no': 'VIT2024099',
                'name': 'Test Student',
                'email': 'test@vit.ac.in',
                'course': 'M.Tech SE',
                'year': 1,
                'cgpa': 8.5
            },
            content_type='application/json')
        assert response.status_code == 201
        data = response.get_json()
        assert data['success'] is True

    def test_add_student_missing_required_field(self, client):
        """POST without required field should return 400."""
        response = client.post('/api/students',
            json={'name': 'Incomplete Student'},
            content_type='application/json')
        assert response.status_code == 400

    def test_delete_student(self, client):
        """DELETE /api/students/<id> should return 200."""
        response = client.delete('/api/students/1')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True


# ─── Courses API Tests ────────────────────────────────────────
class TestCoursesAPI:
    def test_get_courses_returns_200(self, client):
        response = client.get('/api/courses')
        assert response.status_code == 200

    def test_get_courses_has_data(self, client):
        response = client.get('/api/courses')
        data = response.get_json()
        assert len(data['data']) > 0


# ─── Stats API Tests ──────────────────────────────────────────
class TestStatsAPI:
    def test_get_stats_returns_200(self, client):
        response = client.get('/api/stats')
        assert response.status_code == 200

    def test_stats_has_required_fields(self, client):
        response = client.get('/api/stats')
        data = response.get_json()['data']
        assert 'total_students' in data
        assert 'total_courses' in data
        assert 'avg_cgpa' in data


# ─── Utility Function Tests ───────────────────────────────────
class TestUtilities:
    def test_hash_password_returns_string(self):
        result = hash_password('testpassword')
        assert isinstance(result, str)

    def test_hash_password_is_64_chars(self):
        """SHA-256 hex digest is always 64 characters."""
        result = hash_password('anypassword')
        assert len(result) == 64

    def test_same_password_same_hash(self):
        assert hash_password('test') == hash_password('test')

    def test_different_passwords_different_hashes(self):
        assert hash_password('password1') != hash_password('password2')
    def test_health_app_name(self, client):
        """Health response should include app name."""
        response = client.get('/api/health')
        data = response.get_json()
        assert 'app' in data