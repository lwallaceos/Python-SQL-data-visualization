CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    work_year INTEGER,
    experience_level TEXT,
    employment_type TEXT,
    job_title TEXT,
    salary REAL,
    salary_currency TEXT,
    salary_in_usd REAL,
    employee_residence TEXT,
    remote_ratio INTEGER,
    company_location TEXT,
    company_size TEXT
);