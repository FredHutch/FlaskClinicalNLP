import os
from setuptools import setup

PROJECT_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def get_env_variable(var_name, default=False):
    """
    Get the environment variable or return exception
    :param var_name: Environment Variable to lookup
    """
    try:
        return os.environ[var_name]
    except KeyError:
        from io import StringIO
        import configparser
        env_file = os.environ.get('PROJECT_ENV_FILE', PROJECT_ROOT_DIR + "/.env")
        try:
            config = StringIO()
            config.write("[DATA]\n")
            config.write(open(env_file).read())
            config.seek(0, os.SEEK_SET)
            cp = configparser.ConfigParser()
            cp.read_file(config)
            value = dict(cp.items('DATA'))[var_name.lower()]
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            os.environ.setdefault(var_name, value)
            return value
        except (KeyError, IOError):
            if default is not False:
                return default

            error_msg = "Either set the env variable '{var}' or place it in your " \
                        "{env_file} file as '{var} = VALUE'"
            raise EnvironmentError(error_msg.format(var=var_name, env_file=env_file))

setup(
    name='FlaskClinicalNLP',
    version='0.1',
    packages=['flaskclinicalnlp', 'test', 'test.flaskclinicalnlp',],
    url='https://github.com/FredHutch/FlaskClinicalNLP',
    install_requires=['compmed-pkg',
                      'sectionerex',
                      'flask',
                      'boto3',
                      'spacy>=2.2',
                      'scispacy',
                      'en_ner_bionlp13cg_md',
                      'en_core_sci_md'
                      ],
    dependency_links = ["https://{}@github.com/FredHutch/ComprehendMedicalInterface/tarball/master#egg=compmed-pkg"
                            .format(get_env_variable('HDCGITAUTHTOKEN')),
                        "https://{}@github.com/FredHutch/SectionerEx/tarball/master#egg=sectionerex"
                            .format(get_env_variable('HDCGITAUTHTOKEN')),
                        'https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.2.4/en_ner_bionlp13cg_md-0.2.4.tar.gz#egg=en_ner_bionlp13cg_md',
                        'https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.2.4/en_core_sci_md-0.2.4.tar.gz#egg=en_core_sci_md',
                        ],
    license='',
    author='whiteau',
    author_email='whiteau@fredhutch.org',
    description='flask application for several general preprocessing clinical NLP steps (pos tagging, sectioning, NER, etc)',
    zip_safe=False
)
