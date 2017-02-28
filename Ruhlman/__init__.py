#__init__.py

import os
from flask import Flask
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap()

def create_app():
    """Create an application instance."""
    app = Flask(__name__)
    
    # import configuration
    cfg = os.path.join(os.getcwd(), 'config', 'development' + '.py')
    app.config.from_pyfile(cfg)
    
    # initialize extensions
    bootstrap.init_app(app)
    
    # import blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app