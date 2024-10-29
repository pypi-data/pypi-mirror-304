from datetime import datetime
from os import getlogin

def CompareSCE_Status(connection, rows, founds, checks):
    query= f"""
    INSERT INTO CUSTOMS_STATUS(DATE_TIME, USER_ID, NUM_ROWS, NUM_FOUND , NUM_CHECKS, TOOL_USED)
    VALUES ('{datetime.now().date()}','{getlogin()}', '{rows}','{founds}', '{checks}', 'SCE Compare')
    """
    connection.cursor().execute(query)
    connection.commit()
    connection.close()