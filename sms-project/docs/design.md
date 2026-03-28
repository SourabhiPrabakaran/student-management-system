# System Design Document (SDD)
## Student Management System (SMS)
**Version:** 1.0.0 | **Course:** ISWE403L | **Date:** Apr 2026

---

## 1. Architecture

Three-tier web architecture:
- **Frontend:** HTML5/CSS3/JS static pages
- **Backend:** Python Flask REST API
- **Database:** MySQL 8.0

## 2. API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/login | Authenticate user |
| POST | /api/logout | Clear session |
| GET | /api/students | List all students |
| POST | /api/students | Add a student |
| DELETE | /api/students/<id> | Remove a student |
| GET | /api/courses | List all courses |
| GET | /api/stats | Dashboard statistics |
| GET | /api/health | Health check |

## 3. Database Tables

- `users` — Authentication and roles
- `students` — Student records
- `courses` — Course catalog
- `enrollments` — Student-course mappings
- `attendance` — Daily attendance
- `change_log` — SCM audit trail

## 4. Branching Strategy (GitFlow)

- `main` → Production releases
- `develop` → Integration branch
- `feature/*` → Feature development
- `bugfix/*` → Bug fixes
- `hotfix/*` → Critical production fixes
