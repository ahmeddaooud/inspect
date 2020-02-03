import re
import time
from flask import session, redirect, request, render_template, make_response, flash
from sqlalchemy import engine

from inspector.util import tinyid
from tabledef import *
engine = create_engine('sqlite:///inspector.db', echo=True)
from inspector import app, db

from tabledef import User
import hashlib


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
    except:
        return render_template('login.html')
    else:
        return render_template('home.html', recent=expand_recent_bins())


@app.endpoint('views.user_login')
def userlogin():
    return render_template('login.html')


def expand_all_bins():
    all = db.get_bins()
    return all


def count_all_bins():
    count = db.count_bins()
    return count


@app.endpoint('views.admin')
def admin():
    try:
        if session['logged_in'] and session['user_role'] == 'admin':
            return render_template('admin.html', all=expand_all_bins(), count=count_all_bins())
        else:
            return redirect("/")
    except Exception:
        return redirect("/")


@app.endpoint('views.config')
def config():
    try:
        if session['logged_in'] and session['user_role'] == 'admin':
#             config_list = db.get_config()
#             ttl = config_list[0]
#             req_count = config_list[1]
#             prefix = config_list[2]
            config_list = ''
            ttl = ''
            req_count = ''
            prefix = 'PAYFORT'
            return render_template('config.html', ttl=ttl, req_count=req_count, prefix=prefix)
        else:
            return redirect("/")
    except Exception:
        return redirect("/")


@app.endpoint('views.save_config')
def update_config():
    redis_prefix = str(request.form['prefix'])
    max_ttl = request.form['max_ttl']
    max_req_count = request.form['max_req_count']
    db.update_config(max_ttl, max_req_count, redis_prefix)
    flash('Config saved successfully, Still you need to activate new values')
    return redirect("/")

@app.endpoint('views.user_management')
def user_management():
    try:
        if session['logged_in'] and session['user_role'] == 'admin':
            return render_template('user_management.html')
        else:
            return redirect("/")
    except Exception:
        return redirect("/")


@app.endpoint('views.bin_config')
def bin_config():
    name = request.form['name']
    try:
        db.lookup_bin(name)
    except KeyError:
        return "Not found\n", 404
    org_bin = db.get_bin(name)
    org_private = org_bin.private
    org_requests = org_bin.requests
    org_color = org_bin.color
    org_secret_key = org_bin.secret_key
    updated_bin = db.update_bin(org_private,
                                name,
                                request.form['response_msg'],
                                int(float(request.form['response_code'])),
                                int(float(request.form['response_delay'])),
                                org_requests,
                                org_color,
                                org_secret_key)

    return render_template('bin.html',
                           bin=updated_bin,
                           base_url=request.scheme + '://' + request.host)


@app.endpoint('views.bin')
def bin(name):
    handle_automation_names(name)
    try:
        bin = db.lookup_bin(name)
    except KeyError:
        return "Not found\n", 404
    if request.query_string == 'inspect':
        if bin.private and (session.get(bin.name) != bin.secret_key or session.get(bin.name) = 'sleem'):
            return "Private inspector\n", 403
        update_recent_bins(name)
        return render_template('bin.html',
                               bin=bin,
                               base_url=request.scheme + '://' + request.host)
    elif request.query_string.startswith('redirect'):
        db.create_request(bin, request)
        if bin.private and session.get(bin.name) != bin.secret_key:
            return "Private inspector\n", 403
        update_recent_bins(name)
        return render_template('bin.html',
                               bin=bin,
                               base_url=request.scheme + '://' + request.host)
    else:
        db.create_request(bin, request)
        # handel config here
        resp = make_response(bin.response_msg, bin.response_code)
        resp.headers['Provided-By'] = "https://www.payfort.com"
        time.sleep(bin.response_delay)
        return resp


def handle_automation_names(name):
    auto_create = ['AutoNotification', 'AutoRedirectUrl', 'AutoTransactionUrl', 'ahmdaoud', 'AutoReturnSimulator']
    if name in auto_create and not db.bin_exist(name):
        db.create_bin(False, name)
        update_recent_bins(name)


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
        POST_USERNAME = str(request.form['username'])
        sha_phrase = 'secure%hash&inspect'
        POST_PASSWORD = hashlib.sha256(sha_phrase + str(request.form['password'] + sha_phrase)).hexdigest()
        from sqlalchemy.orm import sessionmaker
        Sessionmaker = sessionmaker(bind=engine)
        s = Sessionmaker()
        query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]))
        result = query.first()
        if result:
            session['logged_in'] = True
            session['user_name'] = result.username
            session['user_id'] = result.id
            session['user_role'] = result.userpolicy
            return redirect("/")
        else:
            flash('Invalid login credentials!')
            return redirect("/")
    except Exception:
        return redirect("/")


@app.endpoint('views.logout')
def logout():
    try:
        session['logged_in'] = False
        session['user_id'] = ''
        session['user_name'] = ''
        session['user_role'] = ''
        session.clear()
        return redirect("/")
    except Exception:
        session.clear()
        return redirect("/")


@app.endpoint('views.create_bin')
def create_bin():
    private = request.form.get('private') in ['true', 'on']
    name = str(request.form['name'])
    name = re.sub('[^A-Za-z0-9]+', '', name)

    if name == '':
        name = tinyid()
    else:
        name = name[0:20]

    if db.bin_exist(name):
        flash('\"' + name + '\" ' + 'name is already used, try another one!')
        return redirect("/")
    else:
        bin = db.create_bin(private, name)
        if bin.private:
            session[bin.name] = bin.secret_key
        return redirect('/' + name + '?inspect')
