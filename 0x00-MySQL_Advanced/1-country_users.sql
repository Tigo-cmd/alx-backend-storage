-- AN SQL script that creates a table of users with unique contents
CREATE TABLE IF NOT EXISTS users (
  id NOT NULL AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  name VARCHAR(255),
  country ENUM('US', 'CO', 'TN') NOT NUL DEFAULT 'US'
)