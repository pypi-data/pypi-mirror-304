import oracledb
from pandas import DataFrame
import os


def connectOracel():
    # Get the directory where this script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    instant_client_path = os.path.join(current_dir, 'instantclient')
    oracledb.init_oracle_client(lib_dir=instant_client_path)
    username="A157336"
    password= "hamdiemada157336"
    host= '10.199.104.126'
    port= 1521
    sid= 'analytics'
    connection = oracledb.connect(user=username, password=password, host=host, port=port, sid=sid)
    print("Connection successful.")
    return connection
    
def executeQuery(connection, query, param=None,):
    try:
        with connection.cursor() as cursor:
            # Set session parameters for case-insensitive search
            cursor.execute(query, param)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            return DataFrame(rows, columns=columns)
    except oracledb.DatabaseError as e:
        print("There was a problem executing the query: ", e)
        raise 