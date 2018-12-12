from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.contrib.auth import authenticate, login, logout
from .models import restaurants
from .forms import LoginForm, RegisterForm, SettingsForm, SearchForm
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
    oid = ObjectId(id)
    rest = restaurants.find_one({"_id": oid})
    context = {
        "session": request.session,
        "username": request.session['username'],
        "restaurant": rest,
        "coord0": rest['location']['coordinates'][1],
        "coord1": rest['location']['coordinates'][0]
    }
    return render(request, 'edit_rest.html', context)

def restaurants_view(request):
    

    if request.method == 'GET':
        form = SearchForm(request.GET)
        search = request.GET.get('search')
        keyword = ".*" + str(search) + ".*"
        iterator = restaurants.find({"name": {'$regex': str(keyword)}}).limit(25)
        count = restaurants.find({"name": {'$regex': str(keyword)}}).count()
        print(search)
    else:
        form = SearchForm()
        iterator = restaurants.find().limit(30)
        count = restaurants.find().count()
    context = {
        "session": request.session,
        "username": request.session['username'],
        "restaurants": list(iterator),
        "results": count,
        "form": form
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

