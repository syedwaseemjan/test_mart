#!/bin/bash

# MySQL admin credentials (replace with your actual admin user/password)
ADMIN_USER="root"
ADMIN_PASS=""

# Application database credentials (match alembic.ini)
DB_NAME="ecommerce_db"
APP_USER="test_mart"
APP_PASS="test_mart"


# Check if MySQL is running
if ! mysqladmin ping -u "$ADMIN_USER" ${ADMIN_PASS:+-p"$ADMIN_PASS"} --silent; then
  echo "❌ MySQL server is not running. Start it first with:"
  echo "   brew services start mysql  # macOS"
  echo "   OR"
  echo "   sudo systemctl start mysql  # Linux"
  exit 1
fi

# Connect and execute setup
mysql -u "$ADMIN_USER" ${ADMIN_PASS:+-p"$ADMIN_PASS"} <<EOF
-- Create database
CREATE DATABASE IF NOT EXISTS $DB_NAME 
  CHARACTER SET utf8mb4 
  COLLATE utf8mb4_unicode_ci;

-- Create application user
CREATE USER IF NOT EXISTS '$APP_USER'@'localhost' 
  IDENTIFIED BY '$APP_PASS';

-- Grant permissions
GRANT ALL PRIVILEGES ON $DB_NAME.* 
  TO '$APP_USER'@'localhost';

FLUSH PRIVILEGES;
EOF

echo "Database '$DB_NAME' and user '$APP_USER' initialized successfully!"