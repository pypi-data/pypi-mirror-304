#!/usr/bin/env python3

from dotenv import load_dotenv
from databricks import sql
import os
import argparse

def query(sql_query):
    load_dotenv(".env")
    server_hostname = os.getenv("DATABRICKS_SERVER_HOSTNAME")
    http_path = os.getenv("DATABRICKS_HTTP_PATH")
    access_token = os.getenv("DATABRICKS_TOKEN")

    # Debugging prints
    print(f"Server Hostname: {server_hostname}")
    print(f"HTTP Path: {http_path}")
    print(f"Access Token: {access_token}")

    if not all([server_hostname, http_path, access_token]):
        raise ValueError("One or more environment variables are not set.")

    with sql.connect(
        server_hostname=server_hostname,
        http_path=http_path,
        access_token=access_token,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            result = cursor.fetchall()
            print(len(result))
            for row in result:
                print(row)
            connection.commit()

def main():
    parser = argparse.ArgumentParser(description="Run a SQL query on Databricks.")
    parser.add_argument('sql_query', help='The SQL query to execute.')
    args = parser.parse_args()
    query(args.sql_query)

if __name__ == "__main__":
    main()
