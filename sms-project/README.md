# Student Management System (SMS)

> **Course:** ISWE403L — Software Configuration Management  
> **Programme:** M.Tech Software Engineering, VIT University  
> **Version:** 1.0.0

A web-based student management system demonstrating SCM best practices including version control, change management, CI/CD pipelines, and configuration auditing.

---

## Project Structure

```
student-management-system/
├── src/
│   ├── frontend/
│   │   ├── login.html        # Login page
│   │   ├── dashboard.html    # Main dashboard
│   │   └── students.html     # Student management
│   └── backend/
│       └── app.py            # Flask REST API
├── database/
│   └── schema.sql            # MySQL schema + seed data
├── docs/
│   ├── requirements.md       # SRS document
│   └── design.md             # System design document
├── test/
│   └── test_app.py           # Unit tests (pytest)
├── build/
│   └── build.sh              # Build automation script
├── .github/
│   └── workflows/
│       └── ci.yml            # GitHub Actions CI/CD
└── requirements.txt          # Python dependencies
```

## Running Locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
cd src/backend
python app.py

# 3. Open browser → http://localhost:5000
# Login: admin / admin123
```

## Running Tests

```bash
pytest test/ -v --cov=src/backend
```

## Running the Build Script

```bash
chmod +x build/build.sh
./build/build.sh
```

## SCM Branching Strategy

| Branch | Purpose |
|--------|---------|
| `main` | Production-ready code |
| `develop` | Integration branch |
| `feature/*` | New features |
| `bugfix/*` | Bug fixes |
| `hotfix/*` | Critical production fixes |

## CI/CD Pipeline (GitHub Actions)

Automatically runs on every push and pull request:
1. **Lint** — flake8 code style check
2. **Test** — pytest unit tests with coverage
3. **Validate** — checks all configuration items exist
4. **Security** — pip-audit dependency scan
