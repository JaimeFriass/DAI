from flask import Flask, request, render_template, session, redirect
from jinja2 import Template, Environment, PackageLoader, select_autoescape
from pickleshare import *

''' PICKLESHARE '''
db = PickleShareDB('~/testpickleshare')

app = Flask(__name__)

env = Environment(
	loader=PackageLoader('app', 'templates'),
	autoescape=select_autoescape(['html', 'xml'])
)

""" TEMPLATES """
error_t   = env.get_template('error.html')
article = env.get_template('article.html')
login_t   = env.get_template('login.html')
posts_t     = env.get_template('posts.html')
last_pages     = env.get_template('lastpages.html')
register_t     = env.get_template('register.html')
profile_t     = env.get_template('profile.html')

"""Save current page with log name in db"""
def save_page(log):
    temp = db['pages']
    temp.append(log)
    if len(temp) > 5:
        temp.pop(0)
    db['pages'] = temp
    print(temp)

def init_pages():
    db['pages'] = []

""" Checks if user is logued """
def login_method(request):
    if 'username' not in session:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            if db[username][1] == password:
                session['username'] = username
                init_pages()
                return True
            else:
                print("ERROR AL LOGUEO!!!!!!!!!!!!!!!!!!!")
                return False
        else:
            return True
    else:
        return True



"""////////////  LOGIN PAGE   //////////////"""

@app.route('/login')
def login_page():
    if 'username' in session:
        return redirect("/", code=302)
    print("LOGIN SIN ARGUMENTOS")

    return login_t.render(session=session, login_page=True)

@app.route('/login', methods=['POST'])
def post_login_page():
    if 'username' in session:
        return redirect("/", code=302)

    if not login_method(request):
        error = "Username and password doesn't match in our database."
    else:
        error = ""
        print("Logueado correcto?")
        return redirect("/", code=302)

    return login_t.render(session=session, error = error, login_page = True)

@app.route('/logout', methods=['get', 'post'])
def logout():
    session.pop('username', None)
    return redirect("/", code=302)


@app.route('/register')
def register():
    if 'username' in session:
        return redirect("/", code=302)

    return register_t.render(session=session)


@app.route('/register', methods=['POST'])
def post_register():
    if 'username' in session:
        return redirect("/", code=302)

    error = ""

    if request.method == 'POST':
        if len(request.form.get('username')) > 3:
            db[request.form.get('username')] = [request.form.get('name'),request.form.get('password')]
            session['username'] = request.form.get('username')
            init_pages()
            return redirect("/", code=302)
        else:
            error = "Username too short!"

    return register_t.render(session=session, error=error)

@app.route('/user/<user>', methods=['GET'])
def profile(user):
    return profile_t.render(session=session, profile=db[user], user=user)

"""////////////  MAIN PAGE   //////////////"""

@app.route('/', methods=['get','post'])
def login():
    if 'username' in session:
        save_page("/index")
    else:
        print("/ -> NO SESION")
        if not login_method(request):
            return redirect("/login", code=302)
        return redirect("/login", code=302)
    return article.render(session=session)

"""////////////  POSTS PAGE   //////////////"""

@app.route('/posts', methods=['get','post'])
def posts():
    if 'username' not in session:
        return redirect("/login", 302)

    save_page("/posts")
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

"""////////////  LAST PAGES   //////////////"""

@app.route('/last-pages', methods=['get','post'])
def lastPages():
    if 'username' not in session:
        return redirect("/login", 302)

    return last_pages.render(session = session, pages = db['pages'])
    

@app.errorhandler(404)
def page_not_found(error):
    return error_t.render()

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run(host='0.0.0.0', debug=True)