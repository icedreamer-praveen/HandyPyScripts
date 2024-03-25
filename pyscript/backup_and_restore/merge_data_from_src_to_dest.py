import json
from datetime import datetime

import mysql.connector
import yaml

with open ("env_config/application-dev.yml", "r") as file:
    config = yaml.safe_load(file)

def connect_to_database(host, user, password, database, port):
    """
    Establishes a connection to a MySQL database.

    Args:
        host (str): The hostname or IP address of the MySQL server.
        user (str): The username for accessing the MySQL database.
        password (str): The password for the specified user.
        database (str): The name of the MySQL database to connect to.
        port (str): The port number on which the MySQL server is listening.

    Returns:
        mysql.connector.connection.MySQLConnection or None: A MySQL database connection object if the connection is successful, 
            otherwise None.

    Raises:
        mysql.connector.Error: If an error occurs during the connection process.
        
    Note:
        This function is designed to establish a connection to a MySQL database using the provided credentials and connection details.
        If the connection is successful, a connection object is returned. If any error occurs during the connection attempt, 
        an error message is printed, and None is returned.

    """
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        return connection
    
    except mysql.connector.Error as err:
        print("Error connecting to the database:", err)
        return None
    
field_mapping = {
    "name": "user",
    "created_date": "created_at",
    "intent": "intent",
    "intent_confidence": "intent_confidence",
    "query": "query",
    "query_response": "bot_response",
    "response_type": "response_type",
    "user_identifier": "user_identifier",
    "status": "data_fetch_status",
    "origin": "origin",
    "user_identifier": "user_identifier",
    "username": "username",
    "client": "client",
    "False": "issue"
}

def transfer_data(source_host, source_user, source_password, source_database, source_port,
                  target_host, target_user, target_password, target_database, target_port,
                  table_name_source, table_name_target, field_mapping):
    
    source_connection = connect_to_database(source_host, source_user, source_password, source_database, source_port)
    target_connection = connect_to_database(target_host, target_user, target_password, target_database, target_port)

    if source_connection and target_connection:
        try:
            source_cursor = source_connection.cursor(dictionary=True)
            target_cursor = target_connection.cursor()

            fields_for_check = (field_mapping['created_date'],)
            placeholders = ', '.join(['%s'] * len(fields_for_check))

            source_cursor.execute(f"SELECT * FROM {table_name_source}")
            rows = source_cursor.fetchall()

            for row in rows:
                target_cursor.execute(f"""
                    SELECT COUNT(*) 
                    FROM {table_name_target}
                    WHERE {field_mapping['created_date']} = %s
                """, (row.get('created_date', None),))

                row_count = target_cursor.fetchone()[0]

                if row_count == 0:
                    created_date = row.get("created_date")
                    created_at = created_date if created_date else datetime.now()

                    columns = ', '.join(field_mapping.values())
                    placeholders = ', '.join(['%s'] * len(field_mapping))
                    insert_query = f"INSERT INTO {table_name_target} ({columns}) VALUES ({placeholders})"

                    data_tuple = tuple(
                        row[source_field] if source_field in row else
                        created_at if target_field == "created_at" else
                        json.dumps(row["query_response"]) if target_field == "bot_response" else
                        field_mapping.get(target_field) if target_field != "issue" else
                        False
                        for source_field, target_field in field_mapping.items()
                    )

                    target_cursor.execute(insert_query, data_tuple)

            target_connection.commit()
            print(f"Data transferred from {table_name_source} to {table_name_target} successfully.")

        except mysql.connector.Error as err:
            print("An error occurred:", err)

        finally:
            source_connection.close()
            target_connection.close()
            source_cursor.close()
            target_cursor.close()


source_host = config['datasource']["SOURCE_DATABASE_HOST"]
source_user = config['datasource']["SOURCE_DATABASE_USER"]
source_password = config['datasource']["SOURCE_DATABASE_PASS"]
source_database = config['datasource']["SOURCE_DATABASE_NAME"]
source_port = config['datasource']["SOURCE_DATABASE_PORT"]

target_host = config['datasource']["DATABASE_HOST"]
target_user = config['datasource']["DATABASE_USER"]
target_password = config['datasource']["DATABASE_PASS"]
target_database = config['datasource']["DATABASE_NAME"]
target_port = config['datasource']["DATABASE_PORT"]


transfer_data(source_host, source_user, source_password, source_database, source_port,
              target_host, target_user, target_password, target_database, target_port,
              'source_table', 'destination_table', field_mapping)