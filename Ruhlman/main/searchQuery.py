# searchQuery.py

# executes a search query entered by user in search form

import sqlite3
import os

# original database that Ruhlman website was using
# note: only contains 1998, 1999, 2000, 2001, 2005 or 25% of the database

#path = os.path.dirname(os.path.abspath('Ruhlman/main/searchQuery.py'))
#db_filename = os.path.join(path,'ruhlman_test.db')

# new database that is missing advisors, student majors etc. and generally 
# contains errors
# note: contains most of the data from 20 years of Ruhlman and all submissions

db_filename = '/Users/andreajackson/Desktop/Databases/ruhlman_data.db'
#db_filename = '/Users/andreajackson/Desktop/Databases/ruhlmanSheet.db'

#print "sQ: " + db_filename

from sqliteFunctions import selectSql

def query(query):
    '''query function takes in a string query by user 
    and returns all rows in Search_index that match
    that query'''
    conn3 = sqlite3.connect(db_filename)
    
    # search all columns in Search_all and return a snippet of results with the query highlighted
    SQL_QUERY_all = "SELECT * FROM Search_all WHERE Search_all MATCH ?;"
    SQL_QUERY_ryr = "SELECT * FROM Search_all WHERE year MATCH ?;"
    SQL_QUERY_stu = "SELECT * FROM Search_all WHERE student MATCH ?;"
    SQL_QUERY_maj = "SELECT * FROM Search_all WHERE major MATCH ?;"
    SQL_QUERY_cyr = "SELECT * FROM Search_all WHERE classyear MATCH ?;"
    SQL_QUERY_adv = "SELECT * FROM Search_all WHERE advisor MATCH ?;"
    SQL_QUERY_dept = "SELECT * FROM Search_all WHERE department MATCH ?;"
    SQL_QUERY_title = "SELECT * FROM Search_all WHERE title MATCH ?;"
    SQL_QUERY_abstract = "SELECT * FROM Search_all WHERE abstract MATCH ?;"
    SQL_QUERY_abst_snippet = "SELECT snippet(Search_all,'<mark>','</mark>','...',-1,50) FROM Search_all WHERE abstract MATCH ?"
    
    # make sure the params entered is in a tuple format (param,)
    #snip_results = selectSql(SQL_QUERY_SNIPPETS,conn,(query,))
    query_results_all = selectSql(SQL_QUERY_all,conn3,(query,))
    query_results_ryr = selectSql(SQL_QUERY_ryr,conn3,(query,))
    query_results_stu = selectSql(SQL_QUERY_stu,conn3,(query,))
    query_results_maj = selectSql(SQL_QUERY_maj,conn3,(query,))
    query_results_cyr = selectSql(SQL_QUERY_cyr,conn3,(query,))
    query_results_adv = selectSql(SQL_QUERY_adv,conn3,(query,))
    query_results_dept = selectSql(SQL_QUERY_dept,conn3,(query,))
    query_results_title = selectSql(SQL_QUERY_title,conn3,(query,))
    query_results_abstract = selectSql(SQL_QUERY_abstract,conn3,(query,))
    query_results_abst_snippet = selectSql(SQL_QUERY_abst_snippet,conn3,(query,))
    #query_results_stu = selectSql(SQL_QUERY_students,conn3,(query,))
    #query_results_adv = selectSql(SQL_QUERY_advisors,conn3,(query,))
    #query_results_abs = selectSql(SQL_QUERY_abstracts,conn3,(query,))
    
    conn3.close()
    #return query_results_all, query_results_stu, query_results_adv, query_results_abs 
    return (query_results_all,
           query_results_ryr,
           query_results_stu,
           query_results_maj,
           query_results_cyr,
           query_results_adv,
           query_results_dept,
           query_results_title,
           query_results_abstract,
           query_results_abst_snippet)