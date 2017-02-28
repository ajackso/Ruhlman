# queryDatabase.py

# This script queries the Ruhlman database for info and prepares the data
# for a plotly graph

# written by: Andrea Jackson
# date: July 7, 2016

import sqlite3
import os

# import pandas for easy data manipulation
import pandas as pd
from queries import *

# original database that Ruhlman website was using
# note: only contains 1998, 1999, 2000, 2001, 2005 or 25% of the database

#path = os.path.dirname(os.path.abspath('Ruhlman/main/queryDatabase.py'))
#db_filename = os.path.join(path,'ruhlman_test.db')

# new database that is missing advisors, student majors etc. and generally 
# contains errors
# note: contains most of the data from 20 years of Ruhlman and all submissions

#db_filename = '/Users/andreajackson/Desktop/Databases/ruhlman_data.db'
db_filename = '/Users/andreajackson/Desktop/Ruhlman-Database/database/ruhlmanSheet.db'

#print "qD: " + db_filename

def prepMajorDistData(year):
    '''function queries the ruhlman_test.db, cleans
    up the data and returns a list of tuples of the data'''
    
    conn = sqlite3.connect(db_filename)
    yrList = map(lambda x:str(x),range(1998,2017))
    if year in yrList: 
        year = (str(year),)
        df = pd.read_sql(groupByStudentMajorQueryYearExclude, conn, params = year)
        conn.commit()    
    elif year == 'all':
        df = pd.read_sql(groupByStudentMajorQueryExclude, conn)
        conn.commit()
        
    conn.close()
    
    arch = "Classical and Near Eastern Archaeology"
    wom = "Women's and Gender Studies"
    pea = "Peace and Justice Studies" 
    med = "Media Arts and Sciences"
     
    # clean up data by removing second major and stripping text
    def f(x):
        if (arch not in x and wom not in x and pea not in x and med not in x):
            return x.major.split('and')[0].strip()
        else:
            return x
        
    series = df.apply(f, axis=1) # apply function across the rows of df
    counts = series.value_counts().to_dict()
    
    countsList = []
    for m in sorted(counts, key=counts.get):
        countsList.append((m,counts[m]))
        
    return countsList
    
def prepAdvisorData():
    '''function queries the ruhlman_test.db and groups the submisssions by 
    their advisors. Returns a list of tuples, each one containing the advisors 
    id and a list of the total number of submissions'''
    
    conn = sqlite3.connect(db_filename)
    dfDict = pd.read_sql(groupSubmissionsByAdvisorQuery,conn).to_dict()
    conn.commit()
    
    adv_names = pd.read_sql(lookUpAdvisorNames, conn).to_dict()
    #adv_names = pd.read_sql(lookUpAdvisorInfo, conn).to_dict()
    conn.commit() 
    
    t = []
    for i in range(len(dfDict['advisor_id'])):
        a = adv_names['name'][i].encode('utf-8')
        s = len(dfDict['GROUP_CONCAT(submission_id)'][i].encode('utf-8').split(','))
        print s
        t.append((a,s))
  
    t.sort(key=lambda x: x[1])
    #print dfDict;
    #print adv_names;
    #
    #countStu = {}
    #index = 1
    #for i in dfDict['advisor_id']:
    #    print str(i)
    #    adv = adv_names[i+1]
    #    
    #    countStu[adv] = len(dfDict['GROUP_CONCAT(submission_id)'][i].encode('utf-8').split(','))
    #    index += 1
    #
    #for adv,counts in countStu.iteritems():
    #    t.append((adv,counts))
    #    
    #t.sort(key=lambda x: x[1])
    return t[-30:]
    
def prepAdvisorDataStudents():
    '''function queries the ruhlman_test.db and groups the students by 
    their advisors. Returns a list of tuples, each one containing the advisors 
    id and a list of the total number of students the advisor advised'''
    
    conn = sqlite3.connect(db_filename)
    dfDict = pd.read_sql(groupStudentsByAdvisorQuery,conn).to_dict()
    conn.commit()
    
    adv_names = pd.read_sql(lookUpAdvisorNames, conn).to_dict()
    conn.commit()

    t = []
    for i in range(len(dfDict['advisor_id'])):
        a = adv_names['name'][i].encode('utf-8')
        s = len(dfDict['GROUP_CONCAT(student_id)'][i].encode('utf-8').split(','))
        t.append((a,s))
  
    t.sort(key=lambda x: x[1])
    return t[-30:]
    
#print prepAdvisorDataStudents()
