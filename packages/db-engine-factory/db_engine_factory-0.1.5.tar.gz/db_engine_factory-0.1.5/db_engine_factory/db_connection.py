import os
from sqlalchemy import create_engine
from configparser import ConfigParser

# Load the configuration file
config = ConfigParser()
config.read('db_config.ini')

def create_mysql_engine(db_identifier):
    """
    Creates a MySQL engine using SQLAlchemy with pymysql.
    """
    if db_identifier not in config:
        raise ValueError(f"Database identifier {db_identifier} not found in configuration file.")
    
    db_config = config[db_identifier]
    conn_str = (
        f"mysql+pymysql://{db_config['user']}:{db_config['password']}@"
        f"{db_config['host']}:{db_config.get('port', '3306')}/{db_config['database']}"
    )
    return create_engine(conn_str)

def create_mssql_engine(db_identifier):
    """
    Creates an MSSQL engine using SQLAlchemy with pyodbc.
    """
    if db_identifier not in config:
        raise ValueError(f"Database identifier {db_identifier} not found in configuration file.")

    db_config = config[db_identifier]
    conn_str = (
        f"mssql+pyodbc://{db_config['username']}:{db_config['password']}@"
        f"{db_config['server']}/{db_config['database']}?driver=ODBC+Driver+18+for+SQL+Server"
        "&TrustServerCertificate=yes"
    )
    return create_engine(conn_str)

def create_postgres_engine(db_identifier):
    """
    Creates a PostgreSQL engine using SQLAlchemy with psycopg2.
    """
    if db_identifier not in config:
        raise ValueError(f"Database identifier {db_identifier} not found in configuration file.")
    
    db_config = config[db_identifier]
    conn_str = (
        f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@"
        f"{db_config['host']}:{db_config.get('port', '5432')}/{db_config['database']}"
    )
    return create_engine(conn_str)
