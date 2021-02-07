import os
from flask import Flask
from flask import render_template
from flask.ext.wtf import Form
from wtforms import IntegerField, BooleanField
from random import randint

from pylti.flask import lti
dir = os.path.dirname(os.path.abspath(__file__))
VERSION = '0.0.1'
app = Flask(__name__, static_url_path='', static_folder="frontend", template_folder="frontend")
app.config.from_object('config')

def error(exception=None):
    """ render error page

    :param exception: optional exception
    :return: the error.html template rendered
    """
    return render_template('error.html')


@app.route('/is_up', methods=['GET'])
def hello_world(lti=lti):
    """ Indicate the app is working. Provided for debugging purposes.

    :param lti: the `lti` object from `pylti`
    :return: simple page that indicates the request was processed by the lti
        provider
    """
    return render_template('up.html', lti=lti)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET'])
@app.route('/lti/', methods=['GET', 'POST'])
@lti(request='initial', error=error, app=app)
def index(lti=lti):
    """ initial access page to the lti provider.  This page provides
    authorization for the user.

    :param lti: the `lti` object from `pylti`
    :return: index page for lti provider
    """
    print(lti)
    return render_template('index.html', lti=lti)


def set_debugging():
    """ enable debug logging

    """
    import logging
    import sys

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(name)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

set_debugging()

#if __name__ == '__main__':
"""
For if you want to run the flask development server
directly
"""
port = int(os.environ.get("FLASK_LTI_PORT", 5000))
host = os.environ.get("FLASK_LTI_HOST", "0.0.0.0")
context = (dir+'/server.crt', dir + '/server.key')
print(dir+'/server.crt')
app.run(debug=True, host=host, port=port, ssl_context=context)
