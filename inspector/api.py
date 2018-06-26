import json
import operator

from flask import session, make_response, request, render_template, redirect, url_for

from inspector import app, db
# from inspector.views import expand_recent_bins


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


@app.endpoint('api.bins')
def bins():
    private = request.form.get('private') in ['true', 'on']
    bin = db.create_bin(private)
    if bin.private:
        session[bin.name] = bin.secret_key
    return _response(bin.to_dict())


@app.endpoint('api.delete')
def delete():
    name = request.form['name']
    if 'recent' not in session:
        session['recent'] = []
    if name in session['recent']:
        session['recent'].remove(name)
    session.modified = True
    return render_template('home.html')


@app.endpoint('api.deletebin')
def deletebin():
    req = request.referrer
    req_edit = req.replace(request.url_root, "")
    if "?inspect" in req_edit:
        name = req_edit.replace("?inspect", "")
    if 'recent' not in session:
        session['recent'] = []
    if name in session['recent']:
        session['recent'].remove(name)
    session.modified = True
    return render_template('home.html', recent=expand_recent_bins())

@app.route('/home',methods=['GET','POST'])
def home():
    return render_template('home.html', recent=expand_recent_bins())

@app.endpoint('api.bin')
def bin(name):
    try:
        bin = db.lookup_bin(name)
    except KeyError:
        return _response({'error': "Bin not found"}, 404)

    return _response(bin.to_dict())


@app.endpoint('api.requests')
def requests(bin):
    try:
        bin = db.lookup_bin(bin)
    except KeyError:
        return _response({'error': "Bin not found"}, 404)

    return _response([r.to_dict() for r in bin.requests])


@app.endpoint('api.request')
def request_(bin, name):
    try:
        bin = db.lookup_bin(bin)
    except KeyError:
        return _response({'error': "Bin not found"}, 404)

    for req in bin.requests:
        if req.id == name:
            return _response(req.to_dict())

    return _response({'error': "Request not found"}, 404)


@app.endpoint('api.stats')
def stats():
    stats = {
        'bin_count': db.count_bins(),
        'request_count': db.count_requests(),
        'avg_req_size_kb': db.avg_req_size(), }
    resp = make_response(json.dumps(stats), 200)
    resp.headers['Content-Type'] = 'application/json'
    return resp
