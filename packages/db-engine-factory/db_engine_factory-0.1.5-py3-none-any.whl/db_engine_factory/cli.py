import os
from configparser import ConfigParser
from sqlalchemy import create_engine, text

# Load the configuration file
config = ConfigParser()
config.read('db_config.ini')

def create_engine_from_section(section_name):
    """
    Creates a database engine based on the configuration section.
    """
    if section_name not in config:
        raise ValueError(f"Section {section_name} not found in the configuration file.")

    db_type = config[section_name].get('type')

    if db_type == 'mysql':
        user = config[section_name]['user']
        password = config[section_name]['password']
        host = config[section_name].get('host', 'localhost')
        port = config[section_name].get('port', '3306')
        database = config[section_name]['database']
        conn_str = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

    elif db_type == 'mssql':
        server = config[section_name]['server']
        database = config[section_name]['database']
        username = config[section_name]['username']
        password = config[section_name]['password']
        conn_str = (
            f"mssql+pyodbc://{username}:{password}@{server}/{database}?"
            "driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
        )

    elif db_type == 'postgres':
        user = config[section_name]['user']
        password = config[section_name]['password']
        host = config[section_name].get('host', 'localhost')
        port = config[section_name].get('port', '5432')
        database = config[section_name]['database']
        conn_str = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

    else:
        raise ValueError(f"Unsupported database type {db_type} in section {section_name}")

    return create_engine(conn_str)

def test_connections():
    """
    Tests connections to all databases defined in the configuration file.
    """
    print("[INFO] Starting database connection tests...\n")
    for section in config.sections():
        try:
            engine = create_engine_from_section(section)
            print(f"[INFO] Testing connection to {section}...")
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                for row in result:
                    print(f"[SUCCESS] {section} test query result: {row}")
        except Exception as e:
            print(f"[ERROR] Failed to connect to {section}: {e}")
    print("\n[INFO] Database connection tests completed.")

if __name__ == "__main__":
    test_connections()
