from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.contrib.auth import authenticate, login, logout
from .models import restaurants
from .forms import LoginForm, RegisterForm, SettingsForm, SearchForm, NewRestaurant
from bson.objectid import ObjectId
from django.contrib.auth.models import User

def user_view(request, username):

    context = {
        "profile": User.objects.get(username=username),
        "session": request.session,
        "username": request.session['username']
    }
    return render(request, 'profile.html', context)

def restaurant_view(request, id):

    # Check session
    if 'username' not in request.session:
        return redirect('login')

    oid = ObjectId(id)
    rest = restaurants.find_one({"_id": oid})
    print( rest['location']['coordinates'][0])
    context = {
        "session": request.session,
        "username": request.session['username'],
        "restaurant": rest,
        "coord0": rest['location']['coordinates'][1],
        "coord1": rest['location']['coordinates'][0]
    }
    return render(request, 'view_rest.html', context)

def restaurant_edit(request, id):
    # Check session
    if 'username' not in request.session:
        return redirect('login')

    oid = ObjectId(id)
    rest = restaurants.find_one({"_id": oid})

    data = {
        'name': rest['name'],
        'lat': rest['location']['coordinates'][1],
        'long': rest['location']['coordinates'][0]
    }

    form = NewRestaurant(data)

    if request.method == 'POST':
        form = NewRestaurant(request.POST)

        if form.is_valid():
            coordinates = [form.cleaned_data['lat'], form.cleaned_data['long'] ]
            query = {"_id": oid}
            newvalues = {"$set": {"location": {"coordinates": coordinates, "type": "Point"}, "name": form.cleaned_data['name']} }
            return redirect('/restaurants/view/' + str(rest['_id']))
        else:
            print("ERROR: " + form.errors)
            
    context = {
        "form": form,
        "session": request.session,
        "username": request.session['username'],
        "restaurant": rest,
    }
    return render(request, 'edit_rest.html', context)

def restaurant_delete(request, id):
    # Check session
    if 'username' not in request.session:
        return redirect('login')

    oid = ObjectId(id)
    print(oid)
    restaurants.delete_one({"_id": oid})

    return HttpResponseRedirect('/restaurants/search')

def restaurants_view(request):

    # Check session
    if 'username' not in request.session:
        return redirect('login')
    
    # Initialize forms
    form = SearchForm()
    form_new = NewRestaurant()

    # If new restaurant is sent
    if request.method == 'POST':
        form_new = NewRestaurant(request.POST)

        if form_new.is_valid():
            name = form_new.cleaned_data['name']
            coordinates = [form_new.cleaned_data['lat'], form_new.cleaned_data['long'] ]
            restaurants.insert({"location": {"coordinates": coordinates, "type":"Point"}, "name": name})
        else:
            print("ERROR: " + form_new.errors)


    # If a search keyword is sent by GET method
    if request.GET.get('search'):
        form = SearchForm(request.GET)
        search = request.GET.get('search')
        keyword = ".*" + str(search) + ".*"
        iterator = restaurants.find({"name": {'$regex': str(keyword)}}).limit(30)
        count = restaurants.find({"name": {'$regex': str(keyword)}}).count()

    # View all restaurants
    else:
        iterator = restaurants.find().limit(30)
        count = restaurants.find().count()
    context = {
        "session": request.session,
        "username": request.session['username'],
        "restaurants": list(iterator),
        "results": count,
        "form": form,
        "form_new": form_new
    }
    return render(request, 'restaurants.html', context)

def settings(request):
    if 'username' not in request.session:
        return redirect('login')

    form = SettingsForm()
    if request.method == 'POST':
        form = SettingsForm(request.POST)
        first_name = request.POST.get('first_name')
        password = request.POST.get('password')

        if form.is_valid():
            user = User.objects.get(username=request.session['username'])
            user.password = password
        else:
            print("Error!")

    context = {
        "form": form,
        "session": request.session,
        "username": request.session['username']
        }

    return render(request, 'settings.html', context)


def index(request):
    if 'username' not in request.session:
        return redirect('login')
    
    context = {
        "username": request.session['username'],
        "session": request.session
        }
    return render(request, 'index.html', context)

def test_template(request):
    iterator = restaurants.find().limit(30)
    context = {
        "lista": list(iterator)
    }
    return render(request, 'test.html', context)

def login_action(request):

    if 'username' in request.session:
        print(request.session['username'])
        return redirect('index')

    form = LoginForm()
    context = { 'form': form, 'message': 'Logging in'}

    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            context['message'] = 'Loggued as ' + username
            request.session['username'] = username
            return redirect('index')
        else:
            context['message'] = 'Log error'
    
    return render(request, 'login.html', context)

def logout_action(request):
    try:
        del request.session['username']
    except KeyError:
        pass
    return redirect('/restaurants/login')

def register_action(request):
    form = RegisterForm()
    context = {'form': form, 'message': 'Register in'}

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            context['message'] = "Registered as " + user.username
            return redirect('/login')
        else:
            context['form'] = form
    
    return render(request, 'register.html', context)


# Save current page with log name in DB
def save_page(log):
    actual = session['username']
    if db2.pages.find({"username": actual}).count() > 0:
        db2.pages.update({"username": actual}, {"$push": {"pages": log}})
        if len(db2.pages.find_one({"username": actual})['pages']) > 5:
            db2.pages.update({"username": actual},{"$pop": {"pages": -1}}  )
    else:
        array_nuevo = [log]
        db2.pages.insert({"username": actual, "pages": array_nuevo})
