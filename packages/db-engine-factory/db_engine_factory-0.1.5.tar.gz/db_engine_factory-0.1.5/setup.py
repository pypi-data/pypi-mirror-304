from setuptools import setup, find_packages

setup(
    name='db_engine_factory',
    version='0.1.5',
    packages=find_packages(include=['db_engine_factory', 'db_engine_factory.*']),
    include_package_data=True,
    install_requires=[
        'python-dotenv',
        'SQLAlchemy>=2.0.25',
        'pyodbc',
        'pymysql',
        'psycopg2-binary',
    ],
    entry_points={
        'console_scripts': [
            'test_db_engine_factory = db_engine_factory.cli:test_connections'
        ]
    },
)
