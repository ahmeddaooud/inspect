import json
import urllib2

import yaml
import operator
import re

from flask import session, make_response, request, redirect, render_template, flash

from inspector import app, db
from inspector.util import tinyid
from inspector.views import expand_recent_bins

def _response(object, code=200):
    jsonp = request.args.get('jsonp')
    if jsonp:
        resp = make_response('%s(%s)' % (jsonp, json.dumps(object)), 200)
        resp.headers['Content-Type'] = 'text/javascript'
    else:
        resp = make_response(json.dumps(object), code)
        resp.headers['Content-Type'] = 'application/json'
        resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp



def _safe_form_response(object, code=200):
    jsonp = request.args.get('jsonp')
    if jsonp:
        resp = make_response('%s(%s)' % (jsonp, json.dumps(object)), 200)
        resp.headers['Content-Type'] = 'text/javascript'
    else:
        #FORMAT FORM
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
        resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

def _safe_query_response(object, code=200):
    jsonp = request.args.get('jsonp')
    if jsonp:
        resp = make_response('%s(%s)' % (jsonp, json.dumps(object)), 200)
        resp.headers['Content-Type'] = 'text/javascript'
    else:
        #FORMAT query
        json_format = json.dumps(object)
        resp = make_response(json_format, code)
        resp.headers['Content-Type'] = 'application/json'
        resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp



def _safe_json_response(object, code=200):
    jsonp = request.args.get('jsonp')
    if jsonp:
        resp = make_response('%s(%s)' % (jsonp, json.dumps(object)), 200)
        resp.headers['Content-Type'] = 'text/javascript'
    else:
        #FORMAT JSON
        json_format = json.dumps(object, sort_keys=True, indent=4, separators=(',', ': '))
        json_safe_format = yaml.safe_load(json_format)
        resp = make_response(json_safe_format, code)
        resp.headers['Content-Type'] = 'application/json'
        resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

# @app.endpoint('api.bins')
# def bins():
#     private = request.form.get('private') in ['true', 'on']
#     name = request.form.get('name')
#     name = re.sub('[^A-Za-z0-9]+', '', name)
#
#     if name == '':
#         name = tinyid()
#     else:
#         name = name[0:20]
#
#     if db.bin_exist(name):
#         flash('Duplicate inspector name!')
#         return redirect("/")
#     else:
#         bin = db.create_bin(private, name)
#         if bin.private:
#             session[bin.name] = bin.secret_key
#         return _response(bin.to_dict())


@app.endpoint('api.deletebin')
def deletebin():
    name = request.form['name']
    if 'recent' not in session:
        session['recent'] = []
    if name in session['recent']:
        session['recent'].remove(name)
    session.modified = True
    db.delete_bin(name)
    return render_template('home.html', recent=expand_recent_bins())

@app.endpoint('api.bin')
def bin(name):
    try:
        bin = db.lookup_bin(name)
    except KeyError:
        return _response({'error': "Inspector not found"}, 404)

    return _response(bin.to_dict())


@app.endpoint('api.requests')
def requests(bin):
    try:
        bin = db.lookup_bin(bin)
    except KeyError:
        return _response({'error': "Inspector not found"}, 404)

    return _response([r.to_dict() for r in bin.requests])



@app.endpoint('api.request')
def request_(bin, ref):
    try:
        bin = db.lookup_bin(bin)
    except KeyError:
        return _response({'error': "Inspector not found"}, 404)

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

    return _response({'error': "Request not found"}, 404)




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

