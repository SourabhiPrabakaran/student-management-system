# Software Requirements Specification (SRS)
## Student Management System (SMS)
**Version:** 1.0.0 | **Course:** ISWE403L | **Date:** Apr 2026

---

## 1. Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-01 | System shall allow admin users to log in with username and password | High |
| FR-02 | System shall display a dashboard with student and course statistics | High |
| FR-03 | Admin shall be able to view a list of all students | High |
| FR-04 | Admin shall be able to add new student records | High |
| FR-05 | Admin shall be able to delete student records | Medium |
| FR-06 | System shall display a list of all courses | Medium |
| FR-07 | System shall expose a health-check API endpoint | Low |

## 2. Non-Functional Requirements

| ID | Requirement | Category |
|----|-------------|----------|
| NFR-01 | API response time shall be < 500ms for all endpoints | Performance |
| NFR-02 | Passwords shall be stored using SHA-256 hashing | Security |
| NFR-03 | System shall run on Python 3.8+ with Flask | Compatibility |
| NFR-04 | All source code shall pass flake8 linting | Maintainability |
| NFR-05 | Test coverage shall be ≥ 80% | Quality |
