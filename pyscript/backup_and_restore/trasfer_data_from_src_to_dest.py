import os
import subprocess

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
    

def dump_data(source_host, source_user, source_password, source_database, source_port, table_name, dump_file):
    """
    Dumps data from a specified table in a MySQL database to a SQL file.

    Args:
        source_host (str): The hostname or IP address of the source MySQL server.
        source_user (str): The username for accessing the source MySQL database.
        source_password (str): The password for the specified source MySQL user.
        source_database (str): The name of the source MySQL database containing the table to dump data from.
        source_port (str): The port number on which the source MySQL server is listening.
        table_name (str): The name of the table from which to dump data.
        dump_file (str): The filename for the SQL dump file where the data will be stored.

    Returns:
        None

    Raises:
        subprocess.CalledProcessError: If an error occurs during the subprocess execution.

    Note:
        This function dumps data from the specified table in the source MySQL database to a SQL file using the mysqldump command.
        The dumped data is stored in the specified dump_file. If the dump process is successful, a success message is printed.
        The database connection is closed after the dump process is completed.
    """
    connection = connect_to_database(source_host, source_user, source_password, source_database, source_port)

    if connection:
        try:
            dump_command = f"mysqldump -h{source_host} -u{source_user} -p{source_password} -P{source_port}"
            dump_command += f" --single-transaction --skip-lock-tables {source_database} {table_name} > {dump_file}"

            subprocess.run(dump_command, shell=True, check=True)
            print(f"Data dumped from {source_database}.{table_name} to {dump_file} successfully.")

        except subprocess.CalledProcessError as err:
            print("Error during dump process:", err)

        finally:
            connection.close()


def restore_data(target_host, target_user, target_password, target_database, target_port, table_name, dump_file):
    """
    Restores data from a SQL dump file to a specified table in a MySQL database.

    Args:
        target_host (str): The hostname or IP address of the target MySQL server.
        target_user (str): The username for accessing the target MySQL database.
        target_password (str): The password for the specified target MySQL user.
        target_database (str): The name of the target MySQL database where data will be restored.
        target_port (str): The port number on which the target MySQL server is listening.
        table_name (str): The name of the table where data will be restored.
        dump_file (str): The filename of the SQL dump file from which data will be restored.

    Returns:
        None

    Raises:
        mysql.connector.Error: If an error occurs during the MySQL connection or execution of SQL statements.
        OSError: If an error occurs while accessing or removing the dump file.

    Note:
        This function restores data from a SQL dump file to a specified table in the target MySQL database.
        It reads SQL statements from the dump file, executes them using a cursor, and commits the changes.
        After the restore process is completed, the function closes the database connection and removes the dump file.
    """
    connection = connect_to_database(target_host, target_user, target_password, target_database, target_port)

    if connection:
        try:
            cursor = connection.cursor()

            with open(dump_file, 'r') as f:
                sql_statements = f.read()

                for sql_statement in sql_statements.split(';'):
                    if sql_statement.strip():
                        cursor.execute(sql_statement)

            connection.commit()
            print(f"Data restored from {dump_file} to {target_database}.{table_name} successfully.")

        except mysql.connector.Error as err:
            print("Error during restore process:", err)

        finally:
            connection.close()
            cursor.close()
            
            if os.path.exists(dump_file):
                os.remove(dump_file)


source_host = config['datasource']["SOURCE_DATABASE_HOST"]
source_user = config['datasource']["SOURCE_DATABASE_USER"]
source_password = config['datasource']["SOURCE_DATABASE_PASS"]
source_database = config['datasource']["SOURCE_DATABASE_NAME"]
source_port = config['datasource']["SOURCE_DATABASE_PORT"]
table_name = config['datasource']["TABLE_NAME"]
dump_file = config['datasource']["DUMP_FILE"]

target_host = config['datasource']["DATABASE_HOST"]
target_user = config['datasource']["DATABASE_USER"]
target_password = config['datasource']["DATABASE_PASS"]
target_database = config['datasource']["DATABASE_NAME"]
target_port = config['datasource']["DATABASE_PORT"]


dump_data(source_host, source_user, source_password, source_database, source_port, table_name, dump_file)
restore_data(target_host, target_user, target_password, target_database, target_port, table_name, dump_file)