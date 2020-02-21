# flaskml.py or flaskml/__init__.py
import logging
import os
from flask import Flask, render_template

formatter = logging.Formatter(
    "%(asctime)s %(threadName)-11s %(levelname)-10s %(message)s")

logger = logging.getLogger()
streamhandler = logging.StreamHandler()
streamhandler.setLevel(logging.INFO)
streamhandler.setFormatter(formatter)
logger.addHandler(streamhandler)
logger.setLevel(logging.INFO)


# load medlp interface
from compmed.CompMedServiceInterface import CompMedServiceInterface
import utils.json__parser_util as JSONParser
compMedInterface = CompMedServiceInterface(JSONParser.xform_dict_to_json)

def index():
    return render_template(
        'index.html', name="User")


def create_app(test_config=None):
    # create and configure the flaskml
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.urandom(24),
        DATABASE=os.path.join(app.instance_path, 'flaskclinicalnlp.sqlite'),
    )

    if test_config is None:
        # Now we can access the configuration variables via flaskclinicalnlp.config["VAR_NAME"].
        # Load the default configuration
        #app.config.from_object('config.default')

        # Load the configuration from the instance folder
        '''
        TODO: the is an unexpected interaction between venv, setup.py install, and where instance folders get located in venv
        until this is figured out, the app will rely on a environment var to find the config 
        '''
        #app.config.from_pyfile('config.py')

        # Load the file specified by the APP_CONFIG_FILE environment variable
        # Variables defined here will override those in the default configuration
        app.config.from_envvar('APP_CONFIG_FILE', silent=True)

    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #set up database
    from . import db
    db.init_app(app)


    from flaskclinicalnlp import compmed, sectionerex, spacy
    app.register_blueprint(compmed.bp)
    app.register_blueprint(spacy.bp)
    app.register_blueprint(sectionerex.bp)

    # make url_for('index') == url_for('blog.index')
    # in another flaskclinicalnlp, you might define a separate main index here with
    # flaskclinicalnlp.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule('/', view_func=index)
    app.url_map.strict_slashes = False

    return app


