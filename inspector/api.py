import json
import urllib2

import yaml
from flask import session, make_response, request, redirect, render_template

from inspector import app, db
from inspector.views import expand_recent_bins

from sqlalchemy import *
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from inspector import config

engine = create_engine(config.DATABASE_URL, echo=True)
Base = declarative_base()

def _response(object, code=200):
    jsonp = request.args.get('jsonp')
    if jsonp:
        resp = make_response('%s(%s)' % (jsonp, json.dumps(object)), 200)
        resp.headers['Content-Type'] = 'text/javascript'
    else:
        resp = make_response(json.dumps(object), code)
        resp.headers['Content-Type'] = 'application/json'
        resp.headers['Provided-By'] = "https://www.payfort.com"
        resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


def _safe_form_response(object, code=200):
    jsonp = request.args.get('jsonp')
    if jsonp:
        resp = make_response('%s(%s)' % (jsonp, json.dumps(object)), 200)
        resp.headers['Content-Type'] = 'text/javascript'
    else:
        # FORMAT FORM
        json_format = json.dumps(object, sort_keys=True, indent=4, separators=(',', ': '))
        json_format = json_format.replace('=', '\": \"')
        json_format = json_format.replace('&', '\", \"')
        json_format = json_format.replace('+', ' ')
        json_format = urllib2.unquote(json_format)
        json_format = json_format.replace('\\', '\\\\')
        json_format = json_format.replace('\"{', '{')
        json_format = json_format.replace('}\"', '}')
        json_format = '{' + json_format + '}'
        resp = make_response(json_format, code)
        resp.headers['Content-Type'] = 'application/json'
        resp.headers['Provided-By'] = "https://www.payfort.com"
        resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


def _safe_query_response(object, code=200):
    jsonp = request.args.get('jsonp')
    if jsonp:
        resp = make_response('%s(%s)' % (jsonp, json.dumps(object)), 200)
        resp.headers['Content-Type'] = 'text/javascript'
    else:
        # FORMAT query
        json_format = json.dumps(object)
        resp = make_response(json_format, code)
        resp.headers['Content-Type'] = 'application/json'
        resp.headers['Provided-By'] = "https://www.payfort.com"
        resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


def _safe_json_response(object, code=200):
    jsonp = request.args.get('jsonp')
    if jsonp:
        resp = make_response('%s(%s)' % (jsonp, json.dumps(object)), 200)
        resp.headers['Content-Type'] = 'text/javascript'
    else:
        # FORMAT JSON
        json_format = json.dumps(object, sort_keys=True, indent=4, separators=(',', ': '))
        json_safe_format = yaml.safe_load(json_format)
        resp = make_response(json_safe_format, code)
        resp.headers['Content-Type'] = 'application/json'
        resp.headers['Provided-By'] = "https://www.payfort.com"
        resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.endpoint('api.deletebin')
def deletebin():
    name = request.form['name']
    if 'recent' not in session:
        session['recent'] = []
    if name in session['recent']:
        session['recent'].remove(name)
    session.modified = True
    db.delete_bin(name)
    render_template('home.html', recent=expand_recent_bins())
    return redirect("/")


@app.endpoint('api.bin')
def bin(name):
    engine = create_engine(config.DATABASE_URL, echo=True)
    Base = declarative_base()


########################################################################
    class User(Base):
    """"""
      __tablename__ = "users"

      id = Column(Integer)
      name = Column(String)
      username = Column(String, primary_key=True)
      password = Column(String)
      user_policy = Column(String)
      creation_date = Column(String)
      active = Column(Boolean)

    # ----------------------------------------------------------------------
    def __init__(self, name, username, password, user_policy, creation_date, active):
        """"""
        self.name = name
        self.username = username
        self.password = password
        self.user_policy = user_policy
        self.creation_date = creation_date
        self.active = active


# #  create tables
        Base.metadata.create_all(engine)

        engine = create_engine(config.DATABASE_URL, echo=True)

# #  create a Session
        Sessionmaker = sessionmaker(bind=engine)
        sessionmaker = Sessionmaker()

        user = User("Admin User", "admin@payfort.com", "85abcec2435819f27b76fc72eb9574d49b4d6fe19f70d96ecfbb7ca0efcf7f47", "admin", "08-02-2020", True)
        sessionmaker.add(user)

        user = User("test User", "user@payfort.com", "85abcec2435819f27b76fc72eb9574d49b4d6fe19f70d96ecfbb7ca0efcf7f47", "admin", "08-02-2020", True)
        sessionmaker.add(user)

# user = User("adaoud@payfort.com", "ccee544c307acebbe2d1a1f3ca6f1b9f6519384c40789c04fdf42cfb0516b510", "admin", "08-02-2020", False)
# sessionmaker.add(user)
#
# user = User("adaoud@payfort.com", "93cd8446013be804e0c9a69741aa13be76ac696f9a274789519d40bf19fe723a", "super_user")
# sessionmaker.add(user)
#
# user = User("test@payfort.com", "dd4c210f4869889bd81d9e28391d36e709b89d51d98d8745cffefc2774102d2a", "user")
# sessionmaker.add(user)
#
# # commit the record the database
# sessionmaker.commit()
#
        sessionmaker.commit()
    block = ['listOfBlockedNames']
    if name in block:
        return _response({'error': "Forbidden inspector due to block"}, 403)
    else:
        try:
            bin = db.lookup_bin(name)
        except KeyError:
            return _response({'error': "Inspector not found"}, 206)

        return _response(bin.to_dict())


@app.endpoint('api.requests')
def requests(bin):
    try:
        bin = db.lookup_bin(bin)
    except KeyError:
        return _response({'error': "Inspector not found"}, 206)

    return _response([r.to_dict() for r in bin.requests])


@app.endpoint('api.alljson')
def request_(bin):
    try:
        bin = db.lookup_bin(bin)
    except KeyError:
        return _response({'error': "Inspector not found"}, 206)

@app.endpoint('api.alljson')
def request_(bin):
    try:
        bin = db.lookup_bin(bin)
    except KeyError:
        return _response({'error': "Inspector not found"}, 206)
    return _response([convert_to_json(req) for req in bin.requests])


def convert_to_json(req):
    if req.body != "":
            json_body = req.body
            return _safe_json_response(json_body).json
    elif req.form_data != [] and 'application/x-www-form-urlencoded' in req.content_type:
        if req.raw != "":
            json_raw = req.raw
            return _safe_form_response(json_raw).json
    else:
        for k in req.query_string:
            if req.query_string[k] != {}:
                json_query = req.query_string
                return _safe_query_response(json_query).json


@app.endpoint('api.request')
def request_(bin, ref):
    try:
        bin = db.lookup_bin(bin)
    except KeyError:
        return _response({'error': "Inspector not found"}, 206)

    for req in bin.requests:
        if ref in req.body:
            json_body = req.body
            return _safe_json_response(json_body)
        elif req.form_data != [] and 'application/x-www-form-urlencoded' in req.content_type:
            if ref in req.raw:
                json_raw = req.raw
                return _safe_form_response(json_raw)
        else:
            for k in req.query_string:
                if ref in req.query_string[k]:
                    json_query = req.query_string
                    return _safe_query_response(json_query)

    return _response({'error': "Request not found"}, 206)


@app.endpoint('api.stats')
def stats():
    stats = {
        'Inspectors_count': db.count_bins(),
        'request_count': db.count_requests(),
        'avg_req_size_kb': db.avg_req_size(), }
    resp = make_response(json.dumps(stats), 200)
    resp.headers['Content-Type'] = 'application/json'
    return resp


@app.endpoint('api.inspectors')
def inspectors():
    inspectors = {
        'Inspectors_count': db.count_bins(),
        'Inspectors_names': db.get_bins(), }
    resp = make_response(json.dumps(inspectors), 200)
    resp.headers['Content-Type'] = 'application/json'
    return resp
