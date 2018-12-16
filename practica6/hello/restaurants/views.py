from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.contrib.auth import authenticate, login, logout
from .models import restaurants, Dish
from .forms import LoginForm, RegisterForm, SettingsForm, SearchForm, NewRestaurant, NewDish
from bson.objectid import ObjectId
from django.contrib.auth.models import User

def dish_delete(request, id):
    # Check session
    if 'username' not in request.session:
        return redirect('login')

    Dish.objects.filter(pk=id).delete()
    print(id)

    return HttpResponseRedirect('/restaurants/dishes')

def dishes_view(request):
    # Check session
    if 'username' not in request.session:
        return redirect('login')

    form = NewDish()

    if request.method == 'POST':
        form = NewDish(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            dish_type = form.cleaned_data['dish_type']
            allergens = form.cleaned_data['allergens']
            price = form.cleaned_data['price']
            item = Dish(name=name, dish_type=dish_type, allergens=allergens, price=price)
            item.save()
        else:
            print("ERROR NEW DISH")


    iterator = Dish.objects.all()

    context = {
        "form": form,
        "session": request.session,
        "username": request.session['username'],
        "dishes": Dish.objects.all()
    }
    
    return render(request, 'dishes.html', context)

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
            restaurants.update_one( query, newvalues)
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

    pageNumber = 0
    search = ""
    
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
        
        count = restaurants.find({"name": {'$regex': str(keyword)}}).count()
        
        # If a page number is sent by GET method
        if request.GET.get('p'):
            pageNumber = int(request.GET.get('p'))
            iterator = restaurants.find({"name": {'$regex': str(keyword)}}).skip((pageNumber)*30).limit(30)
        else:
            iterator = restaurants.find({"name": {'$regex': str(keyword)}}).limit(30)
            
    # View all restaurants
    else:
        if request.GET.get('p'):
            pageNumber = int(request.GET.get('p'))
            iterator = restaurants.find().skip((pageNumber)*30).limit(30)
        else:
            iterator = restaurants.find().limit(30)

        count = restaurants.find().count()

    if search != "":
        search = "&search=" + search
        
    context = {
        "session": request.session,
        "username": request.session['username'],
        "restaurants": list(iterator),
        "current_page": pageNumber,
        "search": search,
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
            user.first_name = first_name
            user.password = password
            user.save()
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
