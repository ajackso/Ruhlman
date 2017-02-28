# visualizeDB.py
# this script contains functions that will query a database and generate
# a plotly graph from that query

# written by: Andrea Jackson
# date: July 7, 2016
# update: July 12, 2016

# import plotly modules 
import plotly.graph_objs as go
import json, plotly

# import query functions
from queryDatabase import prepMajorDistData, prepAdvisorData, prepAdvisorDataStudents

def generateTrace(yr):
    counts = []
    # counts for entire distribution of majors for a specific year
    if yr != 0 and yr != 'all':
        counts = prepMajorDistData(yr)
        
    # yr == 'all' --> signifies graph will contain all 20+ ruhlman years
    elif yr == 'all':
        counts = prepMajorDistData(yr)
        
    x = []
    y = []
    # m stands for major
    # c stands for counts
    for m,c in counts:
        x.append(c)
        y.append(m)
        
    trace = go.Bar(
        x=x,
        y=[m.encode('utf-8') for m in y],
        orientation = 'h',
        name="Ruhlman " + str(yr),
        marker=dict(
            color = "rgb(35,82,124)"
        )
    )
    return trace

def genTrace2(countsData):
    x = []
    y = []
    # s stands for submissions or students
    # a stands for advisor 
    for a,s in countsData:
        x.append(s)
        y.append(a)
        
    trace = go.Bar(
        x=x,
        y=y,
        orientation = 'h',
        name="Ruhlman",
        marker=dict(
            color = "rgb(35,82,124)"
        )
    )
    return trace
    
def generateGraph(attr,trace):
    
    layout = go.Layout(
        title = attr['titleName'],
        height = 800,
        xaxis = dict( 
            title=attr['xTitleName']
        ),
        yaxis = dict(                 
            title=attr['yTitleName'],
            autotick=attr['yAutotick']    
        ),
        margin = dict(
        l = 150
        )
    )
    graph = go.Figure(data = [trace], layout = layout)
    graphJSON = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON  
