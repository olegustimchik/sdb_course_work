import mysql.connector
from mysql.connector import Error

class USER:
    def __init__(self, username, user_email, password):
        



def main():
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='comics_store_db',
                                             user='root',
                                             password='Zaika_12345')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)

    except Error as e:
        print("Error while connecting to MySQL", e)

if __name__ == '__main__':
    main()
