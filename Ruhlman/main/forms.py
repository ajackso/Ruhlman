# forms.py

# contains all of the class forms used in the ruhlman mini app

# written by: Andrea Jackson
# date: July 13, 2016 

from flask_wtf import Form
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class graphForm(Form):
    yrMenu = [('blank', 'Choose a year')]
    major_tups = [('1998',1998),('1999',1999),('2000',2000),('2001',2001),('2002',2002),('2003',2003),('2004',2004),('2005',2005),('2006',2006),('2007',2007),('2008',2008),('2009',2009),('2010',2010),('2011',2011),('2012',2012),('2013',2013),('2014',2014),('2015',2015),('2016',2016),('all','All years')]
    yrMenu.extend(major_tups)
    
    qMenu = [('blank', 'Choose a question')]
    question_tups = [('0',"What is the distribution of majors by department?"),('1',"How many presentations have advisors advised?"),('2',"How many students have advisors advised?")]
    qMenu.extend(question_tups)
                                                                                       
    questChoice = SelectField('Analysis Question', choices=qMenu)
    yrChoice = SelectField('Year', choices=yrMenu)
    
    submit = SubmitField('Submit')
    
class searchForm(Form):
    search = StringField('search', validators=[DataRequired()],render_kw={"placeholder": "Search the Ruhlman database"})