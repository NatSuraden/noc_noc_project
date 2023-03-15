import psycopg2
try:
    #connection = psycopg2.connect(user="postgres",password="1234",host="127.0.0.1",port="5432",database="postgres")
    connection = psycopg2.connect(user="postgres",password="pplus1234",host="127.0.0.1",port="5432",database="python2565")
    table = ['accounts','circuit','contract','equipment','event_logs','interface','project','site']
    cursor = connection.cursor()
    for i in table:
        cursor = connection.cursor()
        sql = 'DROP TABLE '+i
        cursor.execute(sql)
        connection.commit()
    # sql = '''DROP table IF EXISTS accounts '''
  
    
    # cursor.execute(sql)
    # connection.commit()
except (Exception, psycopg2.DatabaseError) as error: 
        print(error) 