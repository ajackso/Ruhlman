#run.py

# creates and runs the ruhlman application
# written by: Andrea Jackson
# date: August 11, 2016

from Ruhlman import create_app

if __name__ == '__main__':
    app = create_app()
    app.run()