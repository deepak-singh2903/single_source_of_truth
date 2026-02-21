/* =========================================================
HOW THIS FILE IS USED (VERY SIMPLE)
Local / Server / Cloud — same below command that's it but only once

mysql -u USER -p < hrms_full_schema.sql
 ========================================================= */

/* =========================================================
   HRMS FULL DATABASE SCHEMA
   Authoritative & Locked
   ========================================================= */

DROP DATABASE IF EXISTS hrms_db;
CREATE DATABASE hrms_db;
USE hrms_db;

/* =========================================================
   CORE TABLES
   ========================================================= */

CREATE TABLE companies (
    company_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    company_code VARCHAR(50) UNIQUE NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    official_email_domain VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- Payroll policy
    deduct_employer_pf_from_employee BOOLEAN DEFAULT FALSE,
    deduct_employer_esi_from_employee BOOLEAN DEFAULT FALSE
);

CREATE TABLE roles (
    role_id INT PRIMARY KEY AUTO_INCREMENT,
    role_code VARCHAR(50) UNIQUE NOT NULL,
    role_name VARCHAR(100) NOT NULL,
    description VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO roles (role_code, role_name, description) VALUES
('ADMIN', 'Administrator', 'Full system access'),
('HR', 'Human Resources', 'HR operations'),
('EMPLOYEE', 'Employee', 'Employee dashboard'),
('AUDITOR', 'Auditor', 'Read-only audit access'),
('FINANCE', 'Finance', 'Payroll access');

CREATE TABLE users (
    user_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    company_id BIGINT NOT NULL,
    role_id INT NOT NULL,
    email VARCHAR(255) NULL,
    employee_code VARCHAR(50) NULL,
    login_type ENUM('EMAIL','EMP_CODE') NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    last_login_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE (company_id, email),
    UNIQUE (company_id, employee_code),
    FOREIGN KEY (company_id) REFERENCES companies(company_id),
    FOREIGN KEY (role_id) REFERENCES roles(role_id)
);

/* =========================================================
   EMPLOYEE MASTER (SNAPSHOT ONLY)
   ========================================================= */

CREATE TABLE employee_master (
    employee_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    company_id BIGINT NOT NULL,
    employee_code VARCHAR(50) NOT NULL,

    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    last_name VARCHAR(100) NOT NULL,
    gender ENUM('MALE','FEMALE','OTHER','PREFER_NOT_TO_SAY') NOT NULL,
    date_of_birth DATE NOT NULL,

    guardian_relation_prefix ENUM('S/O','D/O','W/O') NOT NULL,
    guardian_name VARCHAR(255) NOT NULL,

    mobile_number VARCHAR(20) NOT NULL,
    address TEXT NOT NULL,

    date_of_joining DATE NOT NULL,
    department_id BIGINT NOT NULL,
    department_name_snapshot VARCHAR(255) NOT NULL,

    designation_id BIGINT,
    designation_snapshot VARCHAR(255) NOT NULL,

    employment_status ENUM('ACTIVE','ON_HOLD','INACTIVE','EXITED') NOT NULL,
    employment_mode ENUM('PROBATION','CONFIRMED','CONTRACT','TEMPORARY','INTERN','CONSULTANT') NOT NULL,

    aadhar_number VARCHAR(20) NOT NULL,
    pan_number VARCHAR(20) NOT NULL,

    salary_mode ENUM('BANK','CHEQUE') NOT NULL,
    bank_name VARCHAR(255),
    bank_account_number VARCHAR(50),
    ifsc_code VARCHAR(20),
    is_government_account BOOLEAN DEFAULT FALSE,

    is_pf_applicable BOOLEAN DEFAULT FALSE,
    is_esi_applicable BOOLEAN DEFAULT FALSE,
    pf_number VARCHAR(50),
    uan_number VARCHAR(50),
    esi_number VARCHAR(50),

    grade_type ENUM('GRADE','NON_GRADE') NOT NULL,
    is_grade_pay_applicable BOOLEAN DEFAULT FALSE,
    current_basic DECIMAL(12,2) NOT NULL,
    current_ctc DECIMAL(12,2) NOT NULL,

    is_da_applicable BOOLEAN DEFAULT FALSE,
    is_hra_applicable BOOLEAN DEFAULT FALSE,
    is_transport_applicable BOOLEAN DEFAULT FALSE,
    is_medical_applicable BOOLEAN DEFAULT FALSE,
    is_exgratia_applicable BOOLEAN DEFAULT FALSE,
    is_pf_deduction_applicable BOOLEAN DEFAULT FALSE,
    is_esi_deduction_applicable BOOLEAN DEFAULT FALSE,
    is_gratuity_applicable BOOLEAN DEFAULT FALSE,

    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE (company_id, employee_code),
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

/* =========================================================
   HR FORM TABLES (HISTORY)
   ========================================================= */

CREATE TABLE appointment_forms (
    appointment_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    company_id BIGINT NOT NULL,
    employee_id BIGINT NOT NULL,
    grade_type ENUM('GRADE','NON_GRADE') NOT NULL,
    is_grade_pay_applicable BOOLEAN DEFAULT FALSE,
    current_basic DECIMAL(12,2) NOT NULL,
    current_ctc DECIMAL(12,2) NOT NULL,
    salary_mode ENUM('BANK','CHEQUE') NOT NULL,
    bank_name VARCHAR(255),
    bank_account_number VARCHAR(50),
    ifsc_code VARCHAR(20),
    is_government_account BOOLEAN DEFAULT FALSE,
    is_pf_applicable BOOLEAN DEFAULT FALSE,
    is_esi_applicable BOOLEAN DEFAULT FALSE,
    pf_number VARCHAR(50),
    uan_number VARCHAR(50),
    esi_number VARCHAR(50),
    is_da_applicable BOOLEAN DEFAULT FALSE,
    is_hra_applicable BOOLEAN DEFAULT FALSE,
    is_transport_applicable BOOLEAN DEFAULT FALSE,
    is_medical_applicable BOOLEAN DEFAULT FALSE,
    is_exgratia_applicable BOOLEAN DEFAULT FALSE,
    is_pf_deduction_applicable BOOLEAN DEFAULT FALSE,
    is_esi_deduction_applicable BOOLEAN DEFAULT FALSE,
    is_gratuity_applicable BOOLEAN DEFAULT FALSE,
    effective_from_date DATE NOT NULL,
    remarks VARCHAR(255),
    created_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE grade_basic_change_forms (
    change_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    company_id BIGINT NOT NULL,
    employee_id BIGINT NOT NULL,
    grade_type ENUM('GRADE','NON_GRADE') NOT NULL,
    is_grade_pay_applicable BOOLEAN DEFAULT FALSE,
    new_basic DECIMAL(12,2) NOT NULL,
    effective_from_date DATE NOT NULL,
    reason VARCHAR(255),
    created_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE promotion_forms (
    promotion_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    company_id BIGINT NOT NULL,
    employee_id BIGINT NOT NULL,

    new_department_id BIGINT NULL,
    new_department_snapshot VARCHAR(255) NULL,

    new_designation_id BIGINT NOT NULL,
    new_designation_snapshot VARCHAR(255) NOT NULL,

    new_grade_type ENUM('GRADE','NON_GRADE') NOT NULL,
    is_grade_pay_applicable TINYINT(1) DEFAULT 0,

    effective_date DATE NOT NULL,
    remarks VARCHAR(255),

    created_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_promo_employee
        FOREIGN KEY (employee_id)
        REFERENCES employee_master(employee_id)
);


-- =========================
-- Salary Revision History
-- =========================
CREATE TABLE salary_revisions (
    salary_revision_id BIGINT PRIMARY KEY AUTO_INCREMENT,

    company_id BIGINT NOT NULL,
    employee_id BIGINT NOT NULL,

    old_basic DECIMAL(12,2) NOT NULL,
    old_ctc DECIMAL(12,2) NOT NULL,

    new_basic DECIMAL(12,2) NOT NULL,
    new_ctc DECIMAL(12,2) NOT NULL,

    effective_from_date DATE NOT NULL,

    remarks VARCHAR(255),

    created_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_salary_revision_employee
        FOREIGN KEY (employee_id)
        REFERENCES employee_master(employee_id)
);



CREATE TABLE status_change_forms (
    status_change_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    company_id BIGINT NOT NULL,
    employee_id BIGINT NOT NULL,
    employment_status ENUM('ACTIVE','ON_HOLD','INACTIVE','EXITED') NOT NULL,
    effective_from_date DATE NOT NULL,
    reason VARCHAR(255),
    remarks VARCHAR(255),
    created_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE contract_forms (
    contract_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    company_id BIGINT NOT NULL,
    employee_id BIGINT NOT NULL,
    contract_start_date DATE NOT NULL,
    contract_end_date DATE NOT NULL,
    remarks VARCHAR(255),
    created_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE exit_forms (
    exit_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    company_id BIGINT NOT NULL,
    employee_id BIGINT NOT NULL,
    exit_type ENUM('RESIGNATION','TERMINATION','ABSCONDED') NOT NULL,
    resignation_date DATE NOT NULL,
    last_working_date DATE NOT NULL,
    reason VARCHAR(255),
    remarks VARCHAR(255),
    created_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE reimbursement_forms (
    reimbursement_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    company_id BIGINT NOT NULL,
    employee_id BIGINT NOT NULL,
    reimbursement_type VARCHAR(100) NOT NULL,
    reimbursement_amount DECIMAL(12,2) NOT NULL,
    reimbursement_date DATE NOT NULL,
    supporting_document VARCHAR(255),
    remarks VARCHAR(255),
    created_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- Payroll Allowances (Config)
-- =========================
CREATE TABLE payroll_allowances (
    allowance_id BIGINT PRIMARY KEY AUTO_INCREMENT,

    company_id BIGINT NOT NULL,

    allowance_code VARCHAR(50) NOT NULL,   -- HRA, DA, TA, MEDICAL
    allowance_name VARCHAR(100) NOT NULL,

    calculation_type ENUM('PERCENTAGE','FIXED') NOT NULL,
    calculation_value DECIMAL(10,2) NOT NULL,

    is_applicable BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE (company_id, allowance_code),
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);



-- =========================
-- Payroll Deduction Master (Structure Only)
-- =========================
CREATE TABLE payroll_deductions (
    deduction_id BIGINT PRIMARY KEY AUTO_INCREMENT,

    company_id BIGINT NOT NULL,
    deduction_code VARCHAR(50) NOT NULL, -- PF, ESI, PT, TAX
    deduction_name VARCHAR(100) NOT NULL,

    calculation_type ENUM('PERCENTAGE','FIXED','NONE') NOT NULL,
    calculation_value DECIMAL(10,2) NULL,

    is_employee_deduction BOOLEAN DEFAULT TRUE,
    is_employer_deduction BOOLEAN DEFAULT FALSE,

    is_active BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE (company_id, deduction_code)
);



/* =========================================================
   AUDIT LOGS
   ========================================================= */

CREATE TABLE audit_logs (
    audit_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    company_id BIGINT NOT NULL,
    entity_type VARCHAR(100) NOT NULL,
    entity_id BIGINT NOT NULL,
    action_type ENUM('CREATE','UPDATE','STATUS_CHANGE','EXIT') NOT NULL,
    old_value JSON,
    new_value JSON,
    performed_by BIGINT NOT NULL,
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

