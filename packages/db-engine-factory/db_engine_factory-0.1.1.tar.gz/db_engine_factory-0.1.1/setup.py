from setuptools import setup, find_packages

setup(
    name='db-engine-factory',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'python-dotenv',
        'SQLAlchemy>=2.0',
        'pyodbc',
        'pymysql',
        'psycopg2-binary',
    ],
    author='Your Name',
    author_email='your_email@example.com',
    description='A utility for creating SQLAlchemy database engines from config files.',
    url='https://github.com/skyblue-will/db_engine_factory',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'test_db_factory=tests.test:test_connections',
        ],
    },
)
