# Random CRUD
Python script that makes a lot of random operations over a simple table. 
In our case, the table is Customers with the following definition:

```sql 
CREATE TABLE customers 
    (id INTEGER IDENTITY(1001,1) NOT NULL PRIMARY KEY, 
    first_name VARCHAR(255) NOT NULL, 
    last_name VARCHAR(255) NOT NULL, 
    email VARCHAR(255) NOT NULL UNIQUE)
```

## Requeriments
This python script will need: 
* pyodbc. This library required unixodbc. On Mac, just use brew (brew install unixodbc)
* faker. Library that generates random first, last and email addresses in the language you require.

## UnixODBC
Once you have installed unixOdbc on  
```bash
$ odbcinst -j
unixODBC 2.3.7
DRIVERS............: /usr/local/etc/odbcinst.ini
SYSTEM DATA SOURCES: /usr/local/etc/odbc.ini
FILE DATA SOURCES..: /usr/local/etc/ODBCDataSources
USER DATA SOURCES..: /Users/hgalante/.odbc.ini
SQLULEN Size.......: 8
SQLLEN Size........: 8
SQLSETPOSIROW Size.: 8
```
You need to download the SQLServer driver. In order to do that, please refer to this URL and look for the steps of your platform:

* [https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-2017]()

### Test UnixODBC

```bash
sqlcmd -S<server_name> -U<user> -P<passowrd>
```

## 
