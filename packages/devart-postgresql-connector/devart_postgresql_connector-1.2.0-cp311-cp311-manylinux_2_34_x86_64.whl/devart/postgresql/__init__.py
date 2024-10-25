"""
Python Connector for PostgreSQL is a connectivity solution for accessing
PostgreSQL databases from Python applications. It fully implements the Python
DB API 2.0 specification. The connector is distributed as a wheel package
for Windows, macOS, and Linux.
 
Direct connection

    The connector enables you to establish a direct connection to PostgreSQL from
    a Python application via TCP/IP, eliminating the need for the database client
    library. A direct connection increases the speed of data transmission between
    the application and PostgreSQL database server. It also streamlines
    the deployment process since you don't have to distribute any client
    libraries with the application.
 
Secure communication

    The connector supports encrypted communications using SSL/TLS, SSH tunneling,
    and HTTP/HTTPS tunneling.

Version: 1.2.0 

Homepage: https://www.devart.com/python/postgresql/
"""
from .postgresql import *
