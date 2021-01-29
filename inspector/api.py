import json
import urllib2

import yaml
from flask import session, make_response, request, redirect, render_template

from inspector import app, db
from inspector.views import expand_recent_bins


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
    block = ['AutoTransactionUrl']
    return _response('error': "Forbidden inspector due to block"}, 200)


@app.endpoint('api.requests')
def requests(bin):
    try:
        bin = db.lookup_bin(bin)
    except KeyError:
        return _response({'msg': "done"}, 200)
    return _response([r.to_dict() for r in bin.requests])


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
