session['logged_in']

{% if session['logged_in'] %}



import os
import sys
from cStringIO import StringIO

from flask import Flask
from flask_cors import CORS

import config

reload(sys)
sys.setdefaultencoding('utf8')


class WSGIRawBody(object):
    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):
        length = environ.get('CONTENT_LENGTH', '0')
        length = 0 if length == '' else int(length)

        body = environ['wsgi.input'].read(length)
        environ['raw'] = body
        environ['wsgi.input'] = StringIO(body)

        # Call the wrapped application
        app_iter = self.application(environ, self._sr_callback(start_response))

        # Return modified response
        # if not in app_iter
        return app_iter

    def _sr_callback(self, start_response):
        def callback(status, headers, exc_info=None):
            # Call upstream start_response
            start_response(status, headers, exc_info)

        return callback


app = Flask(__name__)

if os.environ.get('ENABLE_CORS', config.ENABLE_CORS):
    cors = CORS(app, resources={r"*": {"origins": os.environ.get('CORS_ORIGINS', config.CORS_ORIGINS)}})

app.wsgi_app = WSGIRawBody(app.wsgi_app)

app.debug = config.DEBUG
app.secret_key = config.FLASK_SESSION_SECRET_KEY
app.root_path = os.path.abspath(os.path.dirname(__file__))

if config.BUGSNAG_KEY:
    import bugsnag
    from bugsnag.flask import handle_exceptions

    bugsnag.configure(
        api_key=config.BUGSNAG_KEY,
        project_root=app.root_path,
        # 'production' is a magic string for bugsnag, rest are arbitrary
        release_stage=config.REALM.replace("prod", "production"),
        notify_release_stages=["production", "test"],
        use_ssl=True
    )
    handle_exceptions(app)

from filters import *

app.jinja_env.filters['status_class'] = status_class
app.jinja_env.filters['friendly_time'] = friendly_time
app.jinja_env.filters['friendly_size'] = friendly_size
app.jinja_env.filters['to_qs'] = to_qs
app.jinja_env.filters['approximate_time'] = approximate_time
app.jinja_env.filters['exact_time'] = exact_time
app.jinja_env.filters['short_date'] = short_date

app.add_url_rule('/', 'views.home')

app.add_url_rule('/<path:name>', 'views.bin',
                 methods=['GET', 'POST', 'DELETE', 'PUT', 'OPTIONS', 'HEAD', 'PATCH', 'TRACE'])

app.add_url_rule('/docs/<name>', 'views.docs')
# app.add_url_rule('/api/bins', 'api.bins', methods=['POST'])
app.add_url_rule('/api/bins/<name>', 'api.bin', methods=['GET'])
app.add_url_rule('/api/delete_inspector', 'api.deletebin', methods=['GET', 'POST'])
app.add_url_rule('/api/v2/<bin>/requests', 'api.requests', methods=['GET'])
app.add_url_rule('/api/v2/<bin>/alljson', 'api.alljson', methods=['GET'])
app.add_url_rule('/api/v1/<bin>/<ref>', 'api.request', methods=['GET'])
app.add_url_rule('/api/stats', 'api.stats')
# app.add_url_rule('/api/inspectors', 'api.inspectors')


app.add_url_rule('/_all_inspectors', 'views.all_inspectors')
app.add_url_rule('/_create_inspector', 'views.create_bin', methods=['POST'])
app.add_url_rule('/_config', 'views.config')
app.add_url_rule('/_save_config', 'views.save_config', methods=['POST'])
app.add_url_rule('/_inspector_config', 'views.bin_config', methods=['POST'])
app.add_url_rule('/_user_login', 'views.user_login')
app.add_url_rule('/_user_management', 'views.user_management')
app.add_url_rule('/_login', 'views.login', methods=['GET', 'POST'])
app.add_url_rule('/_create_user', 'views.create_user', methods=['GET', 'POST'])
app.add_url_rule('/_delete_user', 'views.delete_user', methods=['GET', 'POST'])
app.add_url_rule('/_logout', 'views.logout', methods=['GET'])

# app.add_url_rule('/robots.txt', redirect_to=url_for('static', filename='robots.txt'))

from inspector import api, views
