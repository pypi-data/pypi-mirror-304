from setuptools import setup, find_packages

setup(
    name='databricks_tool',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy<2',
        'python-dotenv',
        'databricks-sql-connector',
    ],
    entry_points={
        'console_scripts': [
            'run-databricks-query=databricks_tool.query_tool:main',
        ],
    },
)