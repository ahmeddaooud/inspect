import json
import time
import urllib
from flask import session, redirect, request, render_template, make_response, flash

from inspector import app, db
all_names = []
allcount = 0

def update_recent_bins(name):
    if 'recent' not in session:
        session['recent'] = []
    if name in session['recent']:
        session['recent'].remove(name)
    session['recent'].insert(0, name)
    if len(session['recent']) > 20:
        session['recent'] = session['recent'][:20]
    session.modified = True



def expand_recent_bins():
    # time.sleep(.2)
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
    try:
        if session['logged_in'] == False:
            return render_template('login.html')
        else:
            return render_template('home.html', recent=expand_recent_bins())
    except Exception:
        return render_template('login.html')




@app.endpoint('views.user_login')
def userlogin():
    return render_template('login.html')


def update_all_bins(name):
    if name not in all_names:
        all_names.insert(0, name)


def expand_all_bins():
    all=[]
    for name in all_names:
        try:
            all.append(db.lookup_bin(name))
        except KeyError:
            all_names.remove(name)

    return all


def count_all_bins():
    count = len(all_names)
    return count


@app.endpoint('views.admin')
def admin():
    if session['logged_in'] == True:
        return render_template('admin.html', all=expand_all_bins(), count=count_all_bins())
    else:
        return home()

@app.endpoint('views.config')
def config():
    if session['logged_in'] == True:
        return render_template('config.html')
    else:
        return home()

@app.endpoint('views.bin_config')
def bin_config():
    name = request.form['name']
    try:
        bin = db.lookup_bin(name)
    except KeyError:
        return "Not found\n", 404
    bin.response_code = int(float(request.form['response_code']))
    bin.response_msg = request.form['response_msg']
    bin.response_delay = float(request.form['response_delay'])
    return render_template('bin.html',
                           bin=bin,
                           base_url=request.scheme + '://' + request.host)

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
        update_all_bins(name)
        return render_template('bin.html',
            bin=bin,
            base_url=request.scheme+'://'+request.host)
    elif 'application/xhtml' in request.headers['Accept']:
        if request.method == 'POST':
             update_recent_bins(name)
             update_all_bins(name)
             db.create_request(bin, request)
             resp = make_response("ok\n")
             resp.headers['Sponsored-By'] = "https://www.payfort.com"
        return render_template('bin.html',
                                   bin=bin,
                                   base_url=request.scheme + '://' + request.host)
    else:
        db.create_request(bin, request)
        # handel config here
        time.sleep(bin.response_delay)
        resp = make_response(bin.response_msg, bin.response_code)
        resp.headers['Sponsored-By'] = "https://www.payfort.com"
        return resp





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


@app.endpoint('views.login')
def login():
    try:
            if request.form['password'] == 'daoud' and request.form['username'] == 'admin@payfort.com':
                session['logged_in'] = True
                return home()
            else:
                flash('Invalid login credentials!')
                return userlogin()
    except Exception:
        return userlogin()



@app.endpoint('views.logout')
def logout():
        session['logged_in'] = False
        return home()
