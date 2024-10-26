import trino
import pandas as pd
from trino.dbapi import connect
from trino.auth import BasicAuthentication
import warnings
from urllib3.exceptions import InsecureRequestWarning


# Suppress SSL warnings
warnings.filterwarnings('ignore', category=InsecureRequestWarning)

class TrinoConnector:
    def __init__(self, host, port, user, password, catalog):
        """
        Initialize the TrinoConnector with connection parameters.
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.catalog = catalog
        self.connection = None

    def connect(self):
        """
        Establish a connection to the Trino server.
        """
        try:
            self.connection = connect(
                host=self.host,
                port=self.port,
                user=self.user,
                auth=BasicAuthentication(self.user, self.password),
                catalog=self.catalog,
                http_scheme='https',
                verify=False
            )
            print("Connection to Trino successful!")
        except Exception as e:
            print(f"Error connecting to Trino: {e}")
            self.connection = None

    def execute_query(self, query):
        """
        Execute a SQL query and return the results as a DataFrame.
        """
        if self.connection is None:
            self.connect()
            if self.connection is None:
                return None
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            cursor.close()
            df = pd.DataFrame(result, columns=columns)
            return df
        except Exception as e:
            print(f"Error executing query: {e}")
            return None

    def close(self):
        """
        Close the Trino connection.
        """
        if self.connection is not None:
            self.connection.close()
            self.connection = None
            print("Trino connection closed.")