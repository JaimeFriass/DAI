from flask import Flask, request, render_template, session, redirect
from jinja2 import Template, Environment, PackageLoader, select_autoescape
from bson import ObjectId
import pymongo

#####    MONGO DB       #####
try:
    conn = pymongo.MongoClient('localhost', 27017)
    print("Connected successfully")
except pymongo.errors.ConnectionFailure:
    print ("Error connecting")

db = conn['test']

db2 = conn.mydb
restaurants = db['restaurants']

####  Flask Config  ####
app = Flask(__name__)
env = Environment(
	loader=PackageLoader('app', 'templates'),
	autoescape=select_autoescape(['html', 'xml'])
)

""" TEMPLATES """
index_t = env.get_template('index.html')
error_t   = env.get_template('error.html')
login_t   = env.get_template('login.html')
posts_t     = env.get_template('posts.html')
last_pages     = env.get_template('lastpages.html')
register_t     = env.get_template('register.html')
profile_t     = env.get_template('profile.html')
restaurants_t = env.get_template('restaurants.html')
view_rest = env.get_template('view_rest.html')
edit_rest = env.get_template('edit_rest.html')
settings_t = env.get_template('settings.html')

"""Save current page with log name in db"""
def save_page(log):
    actual = session['username']
    if db2.pages.find({"username": actual}).count() > 0:
        db2.pages.update({"username": actual}, {"$push": {"pages": log}})
        if len(db2.pages.find_one({"username": actual})['pages']) > 5:
            db2.pages.update({"username": actual},{"$pop": {"pages": -1}}  )
    else:
        array_nuevo = [log]
        db2.pages.insert({"username": actual, "pages": array_nuevo})

""" Checks if user is logued """
def login_method(request):
    if 'username' not in session:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            if db2.users.find({"username":username, "password": password}):
                session['username'] = username
                print("[LOGIN] Logued username: " + session['username'])
                return True
            else:
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

    return login_t.render(session=session, login_page=True)

@app.route('/login', methods=['POST'])
def post_login_page():
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
    print("[LOGIN] Logout username:")
    return redirect("/", code=302)


@app.route('/register')
def register():
    if 'username' in session:
        return redirect("/", code=302)

    return register_t.render(session=session, login_page = True)


@app.route('/register', methods=['POST'])
def post_register():
    if 'username' in session:
        return redirect("/", code=302)

    error = ""
    if request.method == 'POST':
        username = request.form.get('username')
        if len(request.form.get('username')) > 3:
            id = db2.users.insert( {"username": username, "name": request.form.get('name'), "password": request.form.get('password')})
            session['username'] = username
            return redirect("/", code=302)
        else:
            error = "Username too short!"

    return register_t.render(session=session, error=error)

@app.route('/user/<user>', methods=['GET'])
def profile(user):
    if 'username' in session:
        save_page("/user/" + user)

    print(db2.users.find_one({"username": user}))
    print(user)

    return profile_t.render(session=session, profile=db2.users.find_one({"username": user}), user=user)

"""////////////  INDEX PAGE   //////////////"""

@app.route('/')
def index():
    error = ""
    if 'username' in session:
        save_page("/")

    return index_t.render(session=session)

@app.route('/', methods=['post'])
def post_index():
    error = ""
    if 'username' in session:
        save_page("/index")

    if request.method == "POST":
        if len(request.form.get("username")) > 3 and len(request.form.get("password")):
            login_method(request)
        else:
            return redirect("/login", code=302)

    return index_t.render(session=session)


"""////////////  POSTS PAGE   //////////////"""

@app.route('/posts', methods=['get','post'])
def posts():
    if 'username' not in session:
        return redirect("/login", 302)

    save_page("/posts")
    posts = []
    cursor = db2.posts.find()

    for r in cursor:
        posts.append(r)

    return posts_t.render(session=session, posts = posts)
    

@app.route('/newpost', methods=['get','post'])
def newpost():
    if 'username' not in session:
        return redirect("/login", 302)
    if request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text')

    db2.posts.insert({"title": title, "text": text, "user": session['username']})

    return redirect("/posts", 302)

@app.route('/deleteposts', methods=['get','post'])
def deleteposts():
    if 'username' not in session:
        return redirect("/login", 302)
    db2.posts.remove({"user": session['username']})
    return redirect("/posts", 302)

"""////////////  LAST PAGES   //////////////"""

@app.route('/last-pages', methods=['get','post'])
def lastPages():
    if 'username' not in session:
        return redirect("/login", 302)

    save_page('/last-pages')

    return last_pages.render(session = session, pages = db2.pages.find_one({"username": session['username']})['pages'])

"""////////////  RESTAURANTS   //////////////"""

# Restaurants view
# * If GET search is active, view results
# * else view all results
@app.route('/restaurants', methods=['get'])
def search_restaurant():
    if 'username' not in session:
        return redirect("/login", 302)

    name = request.args.get('s', '')

    if len(name) != 0:
        cursor = restaurants.find({"name": {'$regex': name}}).limit(25)
    else:
        cursor = restaurants.find().limit(25)

    array = []

    for r in cursor:
        array.append(r)

    return restaurants_t.render(session = session, restaurants = array, results = cursor.count())

# Restaurant view page
# * View restaurant by *id_rest* id
@app.route('/restaurant/<id_rest>', methods=['GET'])
def restaurant_view(id_rest):
    if 'username' not in session:
        return redirect("/login", 302)

    oid = ObjectId(id_rest)
    rest = restaurants.find_one({"_id": oid})

    return view_rest.render(session = session, restaurant = rest)

# Restaurant edit page
# * Edit restaurant by *id_rest* id
@app.route('/editrestaurant/<id_rest>', methods=['GET'])
def restaurant_edit(id_rest):
    if 'username' not in session:
        return redirect("/login", 302)

    oid = ObjectId(id_rest)
    rest = restaurants.find_one({"_id": oid})

    return edit_rest.render(session = session, restaurant = rest)

# Confirm restaurant edit
# * When edited, this page saves data to DB
@app.route('/saverestaurant', methods=['POST'])
def restaurant_save():
    if 'username' not in session:
        return redirect("/login", 302)

    if request.method == "POST":
        name = request.form.get('name')
        rid = request.form.get('rid')
        coordinates = [ float(request.form.get('lat')), float(request.form.get('long'))]

        if len(name) > 3 and coordinates != None:
            query = {"_id": ObjectId(rid)}
            newvalues = {"$set": {"location": {"coordinates": coordinates, "type": "Point"}, "name": name} }
            print(restaurants.update_one( query, newvalues) )
        else:
            return redirect("/error", 302)

    return redirect("/restaurants", 302)


# Create restaurant
# * Saves data from a new restaurant through a POST method
@app.route('/newrestaurant', methods=['get', 'post'])
def newRestaurant():
    if 'username' not in session:
        return redirect("/login", 302)

    if request.method == "POST":
        name = request.form.get('name')
        coordinates = [float(request.form.get('coord1')), float(request.form.get('coord2'))]
        if len(name) > 3 and coordinates != None:
            restaurants.insert({"location": {"coordinates": coordinates, "type":"Point"}, "name": name})
        else:
            return redirect("/error", 302)

    return redirect("/restaurants", 302)

# Delete restaurant
# * When visited with *id_rest* id, removes it
@app.route('/deleterestaurant/<id_res>', methods=['get'])
def deleteRestaurant(id_res):
    if 'username' not in session:
        return redirect("/login", 302)

    restaurants.delete_one({"_id": ObjectId(id_res)})

    return redirect("/restaurants", 302)

"""////////////  SETTINGS   //////////////"""

@app.route('/settings')
def settings():
    if 'username' not in session:
        return redirect("/login", 302)

    return settings_t.render(session = session)

@app.route('/settings', methods=['post'])
def post_settings():
    if 'username' not in session:
        return redirect("/login", 302)

    save_page('/settings')

    print_name = ""
    print_password = ""

    if request.method == 'POST':
        name = request.form.get('newname')
        password = request.form.get('newpassword')

        if name != '':
            """ Save name """
            print("SESSION USERNAME: " + session['username'])
            print(db2.users.update_one( {"username": session['username']} , { "$set": {"name": name}} ))
            print_name = "Display name changed successfully to " + name + "!"
            
        if password != '':
            db2.users.update_one({"username": session['username']}, { "$set" : {"password": password}})
            print_password = "Password changed successfully!"


    return settings_t.render(session = session, print_name = print_name, print_password = print_password)
    

@app.errorhandler(404)
def page_not_found(error):
    return error_t.render()

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run(host='0.0.0.0', debug=True)