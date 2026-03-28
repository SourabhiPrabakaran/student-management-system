-- ============================================================
-- Student Management System — Database Schema
-- Course: ISWE403L Software Configuration Management
-- Version: 1.0.0
-- Configuration Item: /database/schema.sql
-- ============================================================

CREATE DATABASE IF NOT EXISTS sms_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE sms_db;

-- ─── Users Table ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    username    VARCHAR(50)  NOT NULL UNIQUE,
    password    VARCHAR(255) NOT NULL,  -- SHA-256 hashed
    role        ENUM('admin', 'faculty', 'student') NOT NULL DEFAULT 'student',
    is_active   BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_role (role)
);

-- ─── Students Table ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS students (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    reg_no      VARCHAR(20)  NOT NULL UNIQUE,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(150) NOT NULL UNIQUE,
    phone       VARCHAR(15),
    year        TINYINT NOT NULL DEFAULT 1 CHECK (year BETWEEN 1 AND 4),
    cgpa        DECIMAL(3,1) DEFAULT 0.0 CHECK (cgpa BETWEEN 0.0 AND 10.0),
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_reg_no (reg_no),
    INDEX idx_email (email)
);

-- ─── Courses Table ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS courses (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    code        VARCHAR(20)  NOT NULL UNIQUE,
    name        VARCHAR(150) NOT NULL,
    credits     TINYINT NOT NULL DEFAULT 3,
    faculty     VARCHAR(100),
    semester    VARCHAR(20),
    is_active   BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_code (code)
);

-- ─── Enrollments Table ───────────────────────────────────────
CREATE TABLE IF NOT EXISTS enrollments (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    student_id  INT NOT NULL,
    course_id   INT NOT NULL,
    grade       VARCHAR(5) DEFAULT NULL,
    enrolled_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_enrollment (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id)  REFERENCES courses(id)  ON DELETE CASCADE,
    INDEX idx_student (student_id),
    INDEX idx_course (course_id)
);

-- ─── Attendance Table ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS attendance (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    student_id  INT NOT NULL,
    course_id   INT NOT NULL,
    date        DATE NOT NULL,
    status      ENUM('present', 'absent', 'late') NOT NULL DEFAULT 'present',
    marked_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_attendance (student_id, course_id, date),
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id)  REFERENCES courses(id)  ON DELETE CASCADE
);

-- ─── Change Log Table (SCM Audit Trail) ───────────────────────
CREATE TABLE IF NOT EXISTS change_log (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    table_name  VARCHAR(50)  NOT NULL,
    record_id   INT          NOT NULL,
    action      ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    changed_by  VARCHAR(50)  NOT NULL,
    changed_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    INDEX idx_table (table_name),
    INDEX idx_changed_at (changed_at)
);

-- ─── Seed Data ────────────────────────────────────────────────
INSERT IGNORE INTO users (username, password, role) VALUES
  ('admin',   SHA2('admin123', 256), 'admin'),
  ('faculty1',SHA2('faculty123', 256), 'faculty');

INSERT IGNORE INTO students (reg_no, name, email, phone, year, cgpa) VALUES
  ('VIT2024001', 'Arjun Kumar',   'arjun.k@vit.ac.in',   '9876543210', 1, 8.7),
  ('VIT2024002', 'Priya Sharma',  'priya.s@vit.ac.in',   '9876543211', 1, 9.1),
  ('VIT2024003', 'Rahul Verma',   'rahul.v@vit.ac.in',   '9876543212', 2, 7.8),
  ('VIT2024004', 'Sneha Patel',   'sneha.p@vit.ac.in',   '9876543213', 1, 8.3),
  ('VIT2024005', 'Karthik Rajan', 'karthik.r@vit.ac.in', '9876543214', 2, 9.4);

INSERT IGNORE INTO courses (code, name, credits, faculty, semester) VALUES
  ('ISWE401L', 'Software Architecture',              4, 'Dr. Ramesh', 'Sem-3'),
  ('ISWE402L', 'Advanced Algorithms',                3, 'Dr. Meena',  'Sem-3'),
  ('ISWE403L', 'Software Configuration Management', 3, 'Dr. Suresh', 'Sem-3'),
  ('ISWE404L', 'Cloud Computing',                   4, 'Dr. Anita',  'Sem-3');
