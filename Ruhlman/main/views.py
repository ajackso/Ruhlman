# views.py

# written by: Andrea Jackson
# date: July 8, 2016
# updated: August 22, 2016

#from Ruhlman.main.__init__ import main
from . import main
import os


#if __name__ == '__main__' and __package__ is None:
#    from os import sys, path
#    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# import flask modules
from flask import render_template, request, redirect, url_for

# import jinja2 environment
from jinja2 import Environment 

# import forms
from forms import graphForm, searchForm

# import functions to create graph
from visualizeDB import generateGraph,generateTrace, genTrace2
from graphLayout import attr

from staticImageNames import WCthumbnails

from searchQuery import query
from queryDatabase import prepAdvisorData, prepAdvisorDataStudents
from deptAbbr import deptAbbr as stand_da, variantDeptAbbr as var_da, inv_deptAbbr as inv_da

@main.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')
    
titles = ["Distribution of Student Majors 1998-2016", "Distribution of Majors in "]
@main.route('/explore', methods=['POST', 'GET'])
def explore():         
    gForm = graphForm()
    questChoice, yrChoice = '0','all'
    attr['students']['titleName'] = "Distribution of Student Majors from Ruhlman 1998 to Ruhlman 2016"
    
    barGraphJSON = generateGraph(attr['students'],generateTrace(yrChoice))

    if request.method == 'POST' and gForm.validate_on_submit():
        questChoice = gForm.questChoice.data 
        yrChoice = gForm.yrChoice.data
        if questChoice != "blank" and yrChoice != "blank":
            #What is the distribution of majors by department?
            if questChoice == '0':
                trace = generateTrace(yrChoice)
                if yrChoice != 'all':
                    attr['students']['titleName'] = "Distribution of Student Majors in Ruhlman " + yrChoice
                else:
                    attr['students']['titleName'] = "Distribution of Student Majors from Ruhlman 1998 to Ruhlman 2016"
                barGraphJSON = generateGraph(attr['students'],trace)
        else:
            if questChoice != "blank" and yrChoice == "blank":
                #How many presenations have advisors advised?
                if questChoice == '1':
                    counts = prepAdvisorData()
                    trace = genTrace2(counts)
                    attr['advisors_sub']['titleName'] = "Number of Presentations Professors have Advised from Ruhlman 1998 to Ruhlman 2016"
                    barGraphJSON = generateGraph(attr['advisors_sub'],trace)
                elif questChoice == '2':
                    counts = prepAdvisorDataStudents()
                    trace = genTrace2(counts)
                    attr['advisors_stu']['titleName'] = "Number of Students Professors have Advised from Ruhlman 1998 to Ruhlman 2016"
                    barGraphJSON = generateGraph(attr['advisors_stu'],trace)
                
    return render_template('explore.html', 
                questChoice=questChoice, 
                yrChoice = yrChoice, 
                barGraphJSON = barGraphJSON,
                gForm = gForm,
                WCthumbnails = WCthumbnails)

@main.route('/discover', methods=['POST', 'GET'])
def discover():
    sForm = searchForm() 
    return render_template('discover.html',sForm = sForm)
    
@main.route('/search', methods=['POST','GET'])
def search():
    sForm = searchForm()
    if not sForm.validate_on_submit():
        return redirect(url_for('main.index'))
    return redirect(url_for('main.search_results', searchQuery=sForm.search.data))
    
@main.app_template_filter('departmentAbbr')
def departmentAbbr(fullname):
    '''Function takes in a major or department, finds it's abbreviated form and
    returns HTML markup where the fullname of the major/department is hidden and
    only the abbreviated form is shown'''
    # find the fullname of the department/major and it's abbreviation
    # the fullname may be a variant of the standard name e.g. Media Arts instead
    # of Media Arts & Sciences
    if fullname in var_da:
        abbrValue = var_da[fullname]
    else:
        abbrValue = fullname
        
    if abbrValue in inv_da:
        title = inv_da[abbrValue]
    else:
        title = "None"
    html = '<abbr title = "' + title + '">' + abbrValue + '</abbr>'
    return html

#env = Environment()
#env.filters['departmentAbbr'] = departmentAbbr
  
@main.app_template_filter('highlightQuery')
def highlightQuery(text,query):
    markQuery = "<mark>" + query + "</mark>"
    if (query in text) or (query.lower() in text) or (query.title() in text) or (query.upper() in text):
        finalText_1 = text.replace(query,markQuery)
        finalText_2 = finalText_1.replace(query.lower(),"<mark>" + query.lower() + "</mark>")
        finalText_3 = finalText_2.replace(query.title(),"<mark>" + query.title() + "</mark>")
        finalText = finalText_3.replace(query.upper(),"<mark>" + query.upper() + "</mark>")
        #print "query: " + query
        #print "finalText: " + finalText
        return finalText
    else:
        #print "query: " + query
        #print "text: " + text
        return text
          
@main.route('/search_results/<searchQuery>',methods=['POST','GET'])
def search_results(searchQuery):
    sForm = searchForm()
    all_info,ryr,stu,maj,cyr,adv,dept,title,abstract,snippet = query(searchQuery)
    zip_abst = zip(abstract,snippet)
    columns = [('yr','Year'),('stu','Student'),('maj','Major'),('cla','Class Year'),('adv','Advisor'),('dept','Department'),('titl','Title'),('abs','Abstract')]
    
    #falseCounts = 0
    #Counts = 0
    #for i in range(len(dept)):
    #    stu_maj = dept[i][2]
    #    adv_dept = dept[i][5]
    #    if stu_maj in da:
    #        dept[i]=(dept[i][0],dept[i][1],da[stu_maj],dept[i][3],dept[i][4],dept[i][5],dept[i][6],dept[i][7])
    #        Counts += 1
    #    else:
    #        falseCounts += 1
    #    if adv_dept in da:
    #        dept[i]=(dept[i][0],dept[i][1],dept[i][2],dept[i][3],dept[i][4],da[adv_dept],dept[i][6],dept[i][7])
    #        Counts += 1
    #    else:
    #        falseCounts += 1

    #print [(dept[i][2],dept[i][5]) for i in range(len(dept))]
    #print "falseCounts: " + str(falseCounts)
    #print "Counts: " + str(Counts)
    return render_template('all_search_results.html',
                query_all=all_info,
                query=searchQuery,
                query_ryr=ryr,
                query_stu=stu,
                query_maj=maj,
                query_cyr=cyr,
                query_adv=adv,
                query_dept=dept,
                query_title=title,
                query_abstract=abstract,
                zip_abst=zip_abst,
                columns=columns,
                sForm=sForm
                )
                
@main.route('/interact', methods=['POST', 'GET'])
def interact():
    return render_template('interact.html')
    
@main.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

# updates static files
def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join("/".join(main.root_path.split("/")[:-1]),endpoint,filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)    
