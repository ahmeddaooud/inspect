import urllib
from flask import session, redirect, url_for, escape, request, render_template, make_response

from inspector import app, db, util


def update_recent_bins(name):
    if 'recent' not in session:
        session['recent'] = []
    if name in session['recent']:
        session['recent'].remove(name)
    session['recent'].insert(0, name)
    if len(session['recent']) > 10:
        session['recent'] = session['recent'][:10]
    session.modified = True

# def remove_from_recent(name):
#     if name in session['recent']:
#         session['recent'].remove(name)

def expand_recent_bins():
    if 'recent' not in session:
        session['recent'] = []
    recent = []
    for name in session['recent']:
        try:
            recent.append(db.lookup_bin(name))
        except KeyError:
            session['recent'].remove(name)
            session.modified = True
    return recent


@app.endpoint('views.home')
def home():
    return render_template('home.html', recent=expand_recent_bins())


@app.endpoint('views.bin')
def bin(name):
    try:
        bin = db.lookup_bin(name)
    except KeyError:
        return "Not found\n", 404
    if request.query_string == 'inspect':
        if bin.private and session.get(bin.name) != bin.secret_key:
            return "Private bin\n", 403
        update_recent_bins(name)
        return render_template('bin.html',
            bin=bin,
            base_url=request.scheme+'://'+request.host)
    # if request.url == request.base_url:
    #     return redirect(request.base_url + '?inspect')
    else:
        db.create_request(bin, request)
        if request.headers['Content-Type'] in ['application/json']:
            resp = make_response("ok\n")
            resp.headers['Sponsored-By'] = "https://www.payfort.com"
            return resp
        elif 'application/json' in request.headers['Content-Type']:
            resp = make_response("ok\n")
            resp.headers['Sponsored-By'] = "https://www.payfort.com"
            return resp
        elif 'application/x-www-form' in request.headers['Content-Type']:
            return redirect(request.base_url + '?inspect')
        elif 'form' in request.headers['Content-Type']:
            resp = make_response("ok\n")
            resp.headers['Sponsored-By'] = "https://www.payfort.com"
            return resp
        else:
            return redirect(request.base_url + '?inspect')
            # return render_template('bin.html',
            #                        bin=bin,
            #                        base_url=request.scheme + '://' + request.host)
        # if request.headers['Content-Type'] == 'application/json':
        #     return resp
        # else:


@app.endpoint('views.docs')
def docs(name):
    doc = db.lookup_doc(name)
    if doc:
        return render_template('doc.html',
                content=doc['content'],
                title=doc['title'],
                recent=expand_recent_bins())
    else:
        return "Not found", 404
