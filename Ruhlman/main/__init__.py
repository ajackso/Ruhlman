#__init__.py

# initializes the ruhlman application
# written by: Andrea Jackson
# date: August 11, 2016

from flask import Blueprint

main = Blueprint('main', __name__)

#import the routes
from . import views
#import views
