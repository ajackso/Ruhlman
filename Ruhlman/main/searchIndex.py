# search.py

# this script will provide full-text search functionality for the Ruhlman website
# using sqlite3's fts4 virtual table module 

from sqliteFunctions import exeSql, selectSql
from queries import findAllAlt

import sqlite3
# original db_filename
# '/Users/andreajackson/Desktop/RuhlmanApp/ruhlman_test.db'
#db_filename = '/Users/andreajackson/Desktop/Databases/ruhlman_data.db'
db_filename = '/Users/andreajackson/Desktop/Ruhlman-database/database/ruhlmanSheet.db'

# create search tables
SQL_FTS_all = """
CREATE VIRTUAL TABLE Search_all USING fts4(year,student,major,classyear,advisor,department,title,abstract);
"""

#SQL_FTS_stu = """
#CREATE VIRTUAL TABLE Search_students USING fts4(name, major, year);
#"""

#SQL_FTS_adv = """
#CREATE VIRTUAL TABLE Search_advisors USING fts4(name, department);
#"""

#SQL_FTS_abs = """
#CREATE VIRTUAL TABLE Search_abstracts USING fts4(title, abstract, year);
#"""

# execute sql
exeSql(SQL_FTS_all, sqlite3.connect(db_filename))
print "created a Search_all table"

#exeSql(SQL_FTS_stu, sqlite3.connect(db_filename))
#print "created a Search_students table"

#exeSql(SQL_FTS_adv, sqlite3.connect(db_filename))
#print "created a Search_advisors table"

#exeSql(SQL_FTS_abs, sqlite3.connect(db_filename))
#print "created a Search_abstracts table"

# creates a view table containing all of the columns:
# student_name, major, classyear, year, title, abstract

# create a view 
SQL_CREATEVIEW_all = findAllAlt
#SQL_CREATEVIEW_stu = findStudents
#SQL_CREATEVIEW_adv = findAdvisors
#SQL_CREATEVIEW_abs = findAbstracts

# execute sql
exeSql(SQL_CREATEVIEW_all, sqlite3.connect(db_filename))
print "created a view containing all information (student,advisor,submissions)"

#exeSql(SQL_CREATEVIEW_stu, sqlite3.connect(db_filename))
#print "created a view containing correct student information"

#exeSql(SQL_CREATEVIEW_adv, sqlite3.connect(db_filename))
#print "created a view containing correct advisor information"

#exeSql(SQL_CREATEVIEW_abs, sqlite3.connect(db_filename))
#print "created a view containing correct abstract information"

# use the search feature of fts4 where the query can be checked (MATCH)
# against all of the columns in the Search_all table  

# read view and populate Search_index
SQL_POPULATEINDEX_all = """
INSERT INTO Search_all (year,student,major,classyear,advisor,department,title,abstract)
SELECT year,student,major,classyear,advisor,department,title,abstract
FROM [searchAll]"""

#SQL_POPULATEINDEX_stu = """
#INSERT INTO Search_students (name, major, year)
#SELECT name, major, classyear
#FROM [searchStu]"""

#SQL_POPULATEINDEX_adv = """
#INSERT INTO Search_advisors (name, department)
#SELECT name, department
#FROM [searchAdv]"""

#SQL_POPULATEINDEX_abs = """
#INSERT INTO Search_abstracts (title, abstract, year)
#SELECT title, abstract, year
#FROM [searchAbs]"""

# execute sql
exeSql(SQL_POPULATEINDEX_all, sqlite3.connect(db_filename))
print "populated Search_all with data from view"

#exeSql(SQL_POPULATEINDEX_stu, sqlite3.connect(db_filename))
#print "populated Search_students with data from view"

#exeSql(SQL_POPULATEINDEX_adv, sqlite3.connect(db_filename))
#print "populated Search_advisors with data from view"

#exeSql(SQL_POPULATEINDEX_abs, sqlite3.connect(db_filename))
#print "populated Search_abstracts with data from view"