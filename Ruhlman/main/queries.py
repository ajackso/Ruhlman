# queries.py

# This is a file of query strings stored as variables

# written by: Andrea Jackson
# date: July 11, 2016

groupSubmissionsByAdvisorQuery = '''
        SELECT  advisor_id, 
        GROUP_CONCAT(submission_id) 
        FROM adv_sub_mapping
        GROUP BY advisor_id;'''

lookupProfessorNames = '''
        SELECT t1.name
        FROM advisors t1
        LEFT JOIN 
        (
        SELECT  advisor_id, 
        GROUP_CONCAT(submission_id) 
        FROM adv_sub_mapping
        GROUP BY advisor_id
        ) t2
        on t1.ID = t2.advisor_id;'''
        
lookUpAdvisorNames = '''
        SELECT name 
        FROM advisors
        ORDER BY name;
        '''

lookUpAdvisorInfo = '''
        SELECT id,name 
        FROM advisors;
'''

groupByStudentMajorQuery = '''
        SELECT year,major
        FROM students inner join stu_sub_mapping using (ID) 
        inner join submissions using (ID) 
        WHERE year = ?;'''

groupByStudentMajorQueryYearExclude = '''
        SELECT year,major
        FROM students inner join stu_sub_mapping using (ID) 
        inner join submissions using (ID) 
        where students.major != "Unspecified" AND year = ?;'''
        
groupByStudentMajorQueryAll = '''
        SELECT year,major
        FROM students inner join stu_sub_mapping using (ID) 
        inner join submissions using (ID);'''

groupByStudentMajorQueryExclude = '''
        SELECT year,major
        FROM students inner join stu_sub_mapping using (ID) 
        inner join submissions using (ID) where students.major not in
	(select major from students where major = "Unspecified");'''
        
groupStudentsByAdvisorQuery = '''
        SELECT  advisor_id, GROUP_CONCAT(student_id)
        FROM adv_sub_mapping as t1
        INNER JOIN stu_sub_mapping as t2
        WHERE t1.submission_id = t2.submission_id
        GROUP BY advisor_id;'''
        
searchByStudentInfo = '''
        CREATE VIEW searchStu AS
        SELECT name as student_name,major,classyear,year,title,abstract FROM
        (SELECT *
        FROM students 
        INNER JOIN stu_sub_mapping
        WHERE students.ID = student_id)
        INNER JOIN submissions
        WHERE submissions.ID = submission_id;'''
        
#searchBySubmissionInfo = '''
#        CREATE VIEW seachSub AS
#        SELECT student_ids, year, title, abstract
#        FROM 
#        (SELECT  submission_id, group_concat(student_id) as student_ids
#        from stu_sub_mapping
#        group by submission_id)
#        INNER JOIN submissions
#        WHERE submissions.ID = submission_id;'''
        
searchBySubmissionInfoIncludeNames = '''
        CREATE VIEW seachSub AS
        SELECT name, year, title, abstract
        FROM students ,
        (SELECT student_ids, year, title, abstract
        FROM 
        (SELECT  submission_id, group_concat(student_id) as student_ids
        from stu_sub_mapping
        group by submission_id)
        INNER JOIN submissions
        WHERE submissions.ID = submission_id) as mp
        WHERE  students.ID = mp.student_ids;
        '''
        
findStudents = '''
CREATE VIEW searchStu AS
SELECT name, major, classyear
FROM students ,
        (SELECT student_ids
        FROM 
        (SELECT  submission_id, group_concat(student_id) as student_ids
        from stu_sub_mapping
        group by submission_id)
        INNER JOIN submissions
        WHERE submissions.ID = submission_id) as mp
WHERE  students.ID = mp.student_ids;
        '''
        
findAdvisors = '''
CREATE VIEW searchAdv AS
SELECT name, department
FROM advisors ,
        (SELECT advisor_ids
        FROM 
        (SELECT  submission_id, group_concat(advisor_id) as advisor_ids
        from adv_sub_mapping
        group by submission_id)
        INNER JOIN submissions
        WHERE submissions.ID = advisor_ids) as mp
WHERE  advisors.ID = mp.advisor_ids;
        '''
        
findAbstracts = '''
CREATE VIEW searchAbs AS
SELECT title, abstract, year
FROM submissions;
        '''
findAll = '''
CREATE VIEW searchAll AS
SELECT year, name as student, major, classyear, "name:1" as advisor,department,title,abstract
FROM
(SELECT *
FROM 
(SELECT *
FROM 
(SELECT student_id,smp.submission_id as submission_id,advisor_id
FROM
(select *  from stu_sub_mapping) as smp
JOIN adv_sub_mapping on 
adv_sub_mapping.submission_id = smp.submission_id)
JOIN students ON students.ID = student_id)
JOIN advisors ON advisors.ID = advisor_id)
JOIN submissions on submissions.ID  = submission_id;
        '''
        
findAllAlt = '''
CREATE VIEW searchAll AS
SELECT year, name as student, major, classyear, "name:1" as advisor,department,title,abstract
FROM
(SELECT *
FROM
(SELECT *
FROM
(SELECT ID, sam.student_id,submission_id,advisor_ids
FROM
(select *  from stu_sub_mapping) as ssm
JOIN 
(SELECT  student_id, GROUP_CONCAT(advisor_id) as advisor_ids
FROM stu_sub_mapping as t1
INNER JOIN adv_sub_mapping as t2
WHERE t1.submission_id = t2.submission_id
GROUP BY student_id) AS sam
WHERE
sam.student_id = ssm.student_id)
INNER JOIN students ON students.ID = student_id)
JOIN advisors ON advisors.ID = advisor_ids)
JOIN submissions on submissions.ID  = submission_id;
        '''