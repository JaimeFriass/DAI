from flask import Flask, request, render_template, session, redirect
from jinja2 import Template, Environment, PackageLoader, select_autoescape
from pickleshare import *

''' PICKLESHARE '''
db = PickleShareDB('~/testpickleshare')
db['user'] = "Paco"
db['passwd'] = "Paco"

app = Flask(__name__)

env = Environment(
	loader=PackageLoader('app', 'templates'),
	autoescape=select_autoescape(['html', 'xml'])
)


error_t   = env.get_template('error.html')
article = env.get_template('article.html')
login_t   = env.get_template('login.html')
posts_t     = env.get_template('posts.html')



def login_method(request):
    if 'username' not in session:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            if username == db['user'] and password == db['passwd']:
                session['username'] = username
                return True
            else:
                print("ASDADS")
                return False
        else:
            return True
    else:
        return True


@app.route('/login', methods=['get', 'post'])
def login_page():
    if 'username' in session:
        return redirect("/", code=302)
    
    if not login_method(request):
        error = "Username and password doesn't match in our database."
    else:
        error = ""
        return redirect("/", code=302)

    return login_t.render(session=session, error = error, login_page = True)

@app.route('/logout', methods=['get', 'post'])
def logout():
    session.pop('username', None)
    return redirect("/", code=302)


@app.route('/', methods=['get','post'])
def login():
    if 'username' in session:
        print("/ -> USERNAME: " + session['username'])
    else:
        print("/ -> NO SESION")
        if not login_method(request):
            return redirect("/login", code=302)
    return article.render(session=session)

@app.route('/posts', methods=['get','post'])
def posts():
    if 'username' not in session:
        return redirect("/login", 302)

    posts = db['posts']
    return posts_t.render(session=session, posts = posts)
    

@app.route('/newpost', methods=['get','post'])
def newpost():
    if 'username' not in session:
        return redirect("/login", 302)
    if request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text')

    temp = db['posts']
    temp.append({'title': title, 'text' : text, 'user': session['username']})
    db['posts'] = temp
    return redirect("/posts", 302)

@app.route('/deleteposts', methods=['get','post'])
def deleteposts():
    if 'username' not in session:
        return redirect("/login", 302)
    db['posts'] = []
    return redirect("/posts", 302)


@app.errorhandler(404)
def page_not_found(error):
    return error_t.render()

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run(host='0.0.0.0', debug=True)