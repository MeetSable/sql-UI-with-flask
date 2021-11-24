import psycopg2
from config import config

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
       
	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def get_data(query):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute('set search_path to db')
        cur.execute(query)
        print("The number of parts: ", cur.rowcount)
        row = cur.fetchone()
        rows = []
        while row is not None:
            rows.append(row)
            print(row)
            row = cur.fetchone()
        return rows
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_data(query):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute('set search_path to db')
        cur.execute(query)
        print("The number of parts: ", cur.rowcount)
        print(cur.statusmessage)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        conn.rollback()
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    # data = get_data('employee 5')
    insert_data('insert into departments(department) values(\'hello\');')
