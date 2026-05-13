-- 1. Create the Employee Table
CREATE TABLE IF NOT EXISTS employee (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    department VARCHAR(50),
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'staff'
) ENGINE=InnoDB;

Initial Data Seeding (Optional but Recommended)
-- This creates an initial admin so you can actually log in to create others.
-- The hash below is for the password: 'AdminPassword123'
-- GENERATE YOUR OWN HASH using your security script before running this!
INSERT INTO employee (first_name, last_name, email, department, password_hash, role)
VALUES ('System', 'Admin', 'admin@company.com', 'IT', '$2b$12$ExampleHashKeepThisSecure...', 'admin');