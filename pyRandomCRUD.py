import pyodbc
import random
import sys
import argparse
from faker import Faker
from random import randrange

__version__ = '0.0.3'

class RandomCRUD:

    def __init__(self, language = 'es_MX'):
        self.fake = Faker(language)
        self.driver_name = '{ODBC Driver 13 for SQL Server}'
        self.server_name = 'hgalante-sqlserver-serpro.gce.cloudera.com'
        self.db_user_name= 'sa'
        self.db_password = 'SQL4512!'
        self.db_name = 'CDC_SAMPLE'
        self.column_name_list = ['first_name', 'last_name', 'email']
        self.conn = None
        self._set_connection_database()

    def _set_connection_database(self):
        connection_string = 'Driver={0};SERVER={1};DATABASE={2};UID={3};PWD={4};'
        connection_string = connection_string.format(self.driver_name,self.server_name, self.db_name, self.db_user_name, self.db_password)
        self.conn = pyodbc.connect(connection_string)

    def get_unique_email(self):
        cursor = self.conn.cursor()
        email = self.fake.email()
        sql = "SELECT COUNT(*) FROM CDC_SAMPLE.dbo.customers WHERE email = '{0}'".format(email)
        cursor.execute(sql)
        rows = cursor.fetchall()
        if len(rows) > 0:
            if rows[0][0] > 0:
                return self.get_unique_email()
            else:
                return email
        else:
            return None

    def do_random_insert(self):
        cursor = self.conn.cursor()
        sql = "INSERT INTO Customers(first_name, last_name, email) values ('{0}', '{1}', '{2}')"
        sql = sql.format(self.fake.first_name(), self.fake.last_name(), self.get_unique_email())
        cursor.execute(sql)
        self.conn.commit()

    def do_random_delete(self):
        row_id = self.get_random_row_id()
        if row_id is None:
            return
        cursor = self.conn.cursor()
        sql = "DELETE FROM Customers WHERE ID = '{0}'"
        cursor.execute(sql.format(row_id))
        self.conn.commit()

    def do_random_update(self):
        row_id = self.get_random_row_id()
        if row_id is None:
            return
        column_name = random.choice(self.column_name_list)
        new_value = ''
        new_value = getattr(self.fake, column_name)()
        cursor = self.conn.cursor()
        sql = "UPDATE Customers SET {0} = '{1}' WHERE ID = '{2}'"
        cursor.execute(sql.format(column_name, new_value, row_id))
        self.conn.commit()

    def get_random_row_id(self):
        cursor = self.conn.cursor()
        sql = "SELECT TOP 1 ID FROM CDC_SAMPLE.dbo.customers ORDER BY NEWID();"
        cursor.execute(sql)
        rows = cursor.fetchall()
        if len(rows) > 0:
            return rows[0][0]
        else:
            return None

    def run_operations(self, times = 1):
        for index in range(0, times):
            print('Executing operation number {0}'.format(index + 1))
            operation = randrange(2)
            if operation == 0: #insert
                print(' --> Running a random insert operation')
                self.do_random_insert()
            if operation == 1:  # update
                print(' --> Running a random update operation')
                self.do_random_update()
            if operation == 2:  # delete
                print(' --> Running a random delete operation')
                self.do_random_delete()
        print('{0} total operations run'.format(times))

if __name__ == '__main__':
    description = 'RandomCRUD is a program that produces random CRUD into a ODBC connection for a table.'
    prog = 'randomcrud.exe'
    epilog = 'Developed by Hernan J. Galante <hernan_galante@hotmail.com>. License under Apache License 2.0'
    parser = argparse.ArgumentParser(description=description, prog=prog, epilog=epilog)
    parser.add_argument('--version', action='version', version='%(prog)s {version}'.format(version=__version__))
    parser.add_argument('-s', '--start', dest='start', action='store',
                        help='Start running a random set of operations with a number of times to repeat as argument.')
    args = parser.parse_args()
    n_args = sum([1 for a in vars(args).values() if a])
    if n_args == 0:
        parser.print_help()
        sys.exit(0)
    if args.start:
        try:
            number_ops = int(args.start)
            rop = RandomCRUD()
            rop.run_operations(number_ops)
            sys.exit(0)
        except Exception as e:
            print('*** Error has been detected: {0}'.format(e))
            parser.print_help(sys.stderr)
            sys.exit(0)