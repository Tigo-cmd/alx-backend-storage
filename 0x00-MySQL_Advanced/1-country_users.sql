-- An SQL script that creates a table of users with unique contents
CREATE TABLE IF NOT EXISTS users (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  name VARCHAR(255),
  country CHAR(2) ENUM('US', 'CO', 'TN') NOT NULL DEFAULT 'US'
);