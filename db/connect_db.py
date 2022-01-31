### CONFIGURATION
import sqlite3 as sql
import pandas as pd

### GLOBAL VARIABLES
TABLE_LIST = ['plants']

### FUCNTIONS
def connect_to_db(db_name='house_plants'):
    """
    Desc: Used to establish connection with MYSQL DB
    Input: 
        - db_name(string): Data Base Name
    Output:
        - conn: sqlite3 connection.
    """

    ## Create DB if it does not exist, otherwise create a connection
    conn = sql.connect('{db_name}.db'.format(db_name=db_name))
    
    ## If Table's dont exist, create them
    check_tables(conn)
    
    return conn
    
def check_tables(conn):
    """
    Desc: Checks if tables exists in DB, and creates them if they are not.
    Input: 
        - conn: sqlite3 connection.
    Output: None
    """
    
    ## Run Query to get all Tables in DB
    table_query = "SELECT name FROM sqlite_master WHERE type='table'"
    tdf = pd.read_sql(table_query, conn)
    tableL = tdf['name'].values.tolist()
    
    ## Check if Tables on TABLE_LIST Exist
    for tname in TABLE_LIST:
        
        if tname in tableL:
            continue
        else:
            
            create_table(conn=conn, table_name=tname)
            
def create_table(conn, table_name):
    """
    Desc: Creates Table for Plant Information
    Input: 
        - conn: sqlite3 connection.
        - table_name(string): name of table being created.
    Output: None
    """
    ## Read Plant Sample Data
    table_csv = 'sample_tables\{table_name}.csv'.format(table_name=table_name)
    tdf = pd.read_csv(table_csv, index_col=0)
    
    ## Send Table to DB
    tdf.to_sql("{table_name}_df".format(table_name=table_name), conn, if_exists="replace")
    
    ## Execute Query
    conn.execute(
        """
        CREATE TABLE {table_name} as 
            SELECT * FROM {table_name}_df
        """.format(table_name=table_name)
    )