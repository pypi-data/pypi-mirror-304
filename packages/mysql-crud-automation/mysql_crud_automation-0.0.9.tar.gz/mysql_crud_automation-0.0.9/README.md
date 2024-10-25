
# requirements_dev.txt for the testing
It makes it easier to install and manage dependencies for development and testing, separate from the dependencies required for production.

# difference between requirements_dev.txt and requirements.txt

requirements.txt is used to specify the dependencies required to run the production code of a Python project, while requirements_dev.txt is used to specify the dependencies required for development and testing purposes.

# tox.ini
We use if for the testing in the python package testing against different version of the python 

## how tox works tox enviornment creation
1. Install dependencies and packages 
2. Run commands
3. Its a combination of the (virtualenvwrapper and makefile)
4. It creates a .tox


# pyproject.toml
it is being used for configuration the python project it is a alternative of the setup.cfg file. its contains configuration related to the build system
such as the build tool used package name version author license and dependencies

# setup.cfg
In summary, setup.cfg is used by setup tools to configure the packaging and installation of a Python project

# Testing python application
*types of testing*
1. Automated testing 
2. Manual testing

*Mode of testing*
1. Unit testing
2. Integration tests

*Testing frameworks*

1. pytest
2. unittest
3. robotframework
4. selenium
5. behave
6. doctest

# check with the code style formatting and syntax(coding standard)

1. pylint
2. flake8(it is best because it containt 3 library pylint pycodestyle mccabe)
3. pycodestyle


# How to use the package :-

### Installation :- 

```bash
pip install mysql-crud-automation
```

### Usage :-

```bash
from mysql_connect import mysql_crud
mysql_connector = mysql_crud.mysql_operation(
    host="hostname",
    user="username",
    password="password"
)
```

# CRUD Operation on MySQL :-

### 1. create connection 

```bash
mysql_connector.create_connection()
```

### 2. create database

```bash
mysql_connector.create_database(database_name ="<database_name>")
```

### 3. create table

```bash
create_table_sql = """
CREATE TABLE <table_name> (
    name VARCHAR(100) NOT NULL,   
    age VARCHAR(100) NOT NULL
);"""
mysql_connector.create_table(create_table_sql,database_name)
```

### 4. insert record 

```bash
mysql_connector.insert_single_record(
    record=record:dict,
    table_name="<table_name>", 
    database_name='<database_name>'
    )
```

### 5. insert multiple record 

```bash
mysql_connector.insert_multiple_records(
    record= [record:dict],
    table_name= "<table_name>", 
    database_name= '<database_name>'
    )
```

### 6. bulk insert record 

- in this datafile is in .csv or .xlsx file 

```bash
mysql_connector.bulk_insert(
    datafile="<file_path>", 
    table_name="<table_name>",
    database_name='<database_name>', 
    unique_field=<'column_name'>
)
```
 
### 7. find query  

```bash
mysql_connector.find(
    query:dict = {}, 
    table_name="<table_name>", 
    database_name='<database_name>'
)
```
### 8. find all query in the table 

```bash
mysql_connector.find(
    table_name="<table_name>", 
    database_name='<database_name>'
)
```

### 8. update query

```bash
mysql_connector.update(
    query: dict={}, 
    new_values: dict={}, 
    table_name="<table_name>", 
    database_name='<database_name>'
)
```

### 9. delete query

```bash
mysql_connector.delete(
    query: dict={}, 
    table_name="<table_name>", 
    database_name='<database_name>'
)
```
