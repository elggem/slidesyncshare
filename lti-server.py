import os
from flask import Flask
from flask import render_template
from flask import request
from flask.ext.wtf import Form
from wtforms import IntegerField, BooleanField
from random import randint
from hashlib import sha3_256

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
    print("LTI_help: ", lti)
    lti_para = request.form
    pw = sha3_256((lti_para.get('tool_consumer_instance_guid') + lti_para.get('context_id') + lti_para.get(
        'resource_link_id')).encode('utf-8')).hexdigest()
    context = {}
    context.update({'room_name': lti_para.get('resource_link_title', 'Conference'),
                    'user_name': lti_para.get('lis_person_name_full', 'User'),
                    'email': lti_para.get('lis_person_contact_email_primary'),
                    'pw': pw})
    print(pw)
    return render_template('index.html', lti=context)


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

# if __name__ == '__main__':
"""
For if you want to run the flask development server
directly
"""
port = int(os.environ.get("FLASK_LTI_PORT", 5000))
host = os.environ.get("FLASK_LTI_HOST", "0.0.0.0")
context = (dir + '/certs/server.crt', dir + '/certs/server.key')
print(dir + '/server.crt')
app.run(debug=True, host=host, port=port, ssl_context=context)
