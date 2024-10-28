# DBEngineFactory

**Version**: 0.1.0  
**Author**: Will Palmer  
**Description**: `DBEngineFactory` is a Python library that simplifies connecting to multiple database types (MySQL, MSSQL, PostgreSQL) through SQLAlchemy, with connections managed via a centralized configuration file. This library is designed to streamline database management for applications that work across diverse database systems.

---

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Creating Database Engines](#creating-database-engines)
  - [Testing Connections](#testing-connections)
- [Example AI Prompt for Assistance](#example-ai-prompt-for-assistance)
- [Running Tests](#running-tests)
- [Contributing](#contributing)

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/willpalmer81/db_engine_factory.git
   cd db_engine_factory
   ```

2. **Install the package**:
   ```bash
   pip install .
   ```

   This installs the package and dependencies:
   - `python-dotenv`
   - `SQLAlchemy>=2.0`
   - `pyodbc`
   - `pymysql`
   - `psycopg2-binary`

3. **Create a configuration file**: Ensure your `.ini` configuration file (e.g., `db_config.ini`) is in the project root or the directory you run scripts from.

## Configuration

### Setting Up Your `.ini` Configuration File

Create a `.ini` file (e.g., `db_config.ini`) in the project’s root directory. Each section should represent a different database configuration.

#### Example `db_config.ini`

```ini
# MySQL Database
[mysql_db]
type = mysql
user = myuser
password = mypassword
host = localhost
port = 3306
database = mydatabase

# MSSQL Database
[mssql_db]
type = mssql
server = sqlserver.example.com
database = mydatabase
username = myuser
password = mypassword

# PostgreSQL Database
[postgres_db]
type = postgres
user = myuser
password = mypassword
host = localhost
port = 5432
database = mydatabase
```

**Explanation of Fields**

- **type**: Type of database (`mysql`, `mssql`, or `postgres`).
- **user / username**: Database username.
- **password**: Database password.
- **host / server**: Database server address.
- **port**: Database port (default is `3306` for MySQL and `5432` for PostgreSQL).
- **database**: The name of the database.

## Usage

### Creating Database Engines

Use the functions provided in `db_connection.py` to create database engines. Each function takes a `db_identifier`, which should match the section name in the `.ini` configuration file.

```python
from db_engine_factory.db_connection import create_mysql_engine, create_mssql_engine, create_postgres_engine

# Create a MySQL engine
mysql_engine = create_mysql_engine("mysql_db")

# Create an MSSQL engine
mssql_engine = create_mssql_engine("mssql_db")

# Create a PostgreSQL engine
postgres_engine = create_postgres_engine("postgres_db")
```

### Function Parameters

- **create_mysql_engine(db_identifier)**: Creates a MySQL engine based on the configuration in `db_config.ini`.
- **create_mssql_engine(db_identifier)**: Creates an MSSQL engine using the specified configuration.
- **create_postgres_engine(db_identifier)**: Creates a PostgreSQL engine according to the configuration provided.

### Testing Connections

You can test connections to all configured databases using the command-line script `test_db_engine_factory`, which runs a `SELECT 1` query for each configured database.

```bash
test_db_engine_factory
```

This command outputs success or error messages for each database connection attempt, which is useful for confirming that your `.ini` file is configured correctly.

## Example AI Prompt for Assistance

Here’s a sample prompt you can use with an AI assistant to get help:

> "I'm using `DBEngineFactory` to connect to MySQL, MSSQL, and PostgreSQL databases. I’ve set up my database configurations in a `.ini` file under sections like `[mysql_db]`, `[mssql_db]`, and `[postgres_db]`. I use the functions `create_mysql_engine(db_identifier)`, `create_mssql_engine(db_identifier)`, and `create_postgres_engine(db_identifier)`. Can you help troubleshoot connection issues or assist in verifying query results?"

This provides the AI assistant with key details about your setup, making it easier for them to offer targeted help.

## Running Tests

The package includes a test script `test.py` for verifying connections to databases specified in the `.ini` file.

To run the tests:

1. Confirm your `.ini` file is correctly configured.
2. Execute the test command:
   ```bash
   test_db_engine_factory
   ```

This script will attempt a connection to each database and perform a `SELECT 1` query, with the connection results shown in the console.

## Contributing

To contribute to `DBEngineFactory`:

1. **Fork** the repository.
2. **Create a branch** (`git checkout -b feature/YourFeature`).
3. **Commit your changes** (`git commit -m 'Add a new feature'`).
4. **Push to the branch** (`git push origin feature/YourFeature`).
5. **Open a pull request**.

If you encounter any issues or have feature suggestions, please [open an issue on GitHub](https://github.com/willpalmer81/db_engine_factory/issues).

---
