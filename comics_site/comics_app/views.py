# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from .models import *
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.db import connections
from .forms import *
from django.conf import settings
import os
from .map import *

def home_page_(request):

    comics_item = COMICS.objects.order_by('comics_id')[0:4]
    return render(request, "home.html", {'comics_item': comics_item})

def search_page(request):
    if (request.method == "POST"):
        comics_item = None
        search_data = request.POST["search-data"]
        if(search_data):
            comics_item = COMICS.objects.filter(comics_t__icontains=search_data)
        return render(request, "search_comics.html", {"comics_item":comics_item})
    else:
        comics_item = COMICS.objects.raw("SELECT comics_id, path_image, title, comics_amount FROM comics ORDER BY title limit 3;")
        return render(request, "search_comics.html", {"comics_item":comics_item})

def inspect_field(_field):
    if (_field == ""):
        return None
    return _field

# def MapFormToUser(form):
#     user = USER()
#     user.user_name = form.cleaned_data['name']
#     user.user_lastname = form.cleaned_data["lastname"]
#     user.user_login = form.cleaned_data["login"]
#     user.password = form.cleaned_data["password_2"]
#     user.user_mobile = form.cleaned_data["mobile"]
#     user.user_email = form.cleaned_data["email"]
#     return user


def registration_page(request):
    ''' Ragisration user and set some inf in a session(login, role(default user), number) '''

    if (request.method == "POST"):
        storage = messages.get_messages(request)
        storage.usage = True
        form = UserInfForm(request.POST)
        if (form.is_valid()):
            user = MapFormToUser(form)

            request.session['user_login'] = user.user_login  # set user login in a session
            request.session['user_role'] = 2 # set user role on a session
            request.session['user_name'] = user.user_name # set user name
            request.session['user_lastname'] = user.user_lastname # set user lastname
            request.session['user_mobile'] = user.user_mobile
            messages.success(request, "Your account created.")
            cursor = connections['default'].cursor()
            cursor.execute(f'CALL insert_USER("{user.user_name}", "{user.user_lastname}", "{user.user_login}","{user.user_email}", "{user.user_mobile}","{user.password}")')
            return redirect("homepage")
    else:
        form = UserInfForm()
    return render(request, "user/registration.html", {"form":form})

def sign_in(request):
    '''                 SIGN IN USER
        Set user information in django sesion, if user already signs in '''
    storage = messages.get_messages(request)
    storage.usage = True
    if (request.method == 'POST'):
        form = UserSignInForm(request.POST)
        if (form.is_valid()):
            user = MapSignFormToUser(form)
            SetUserInSession(request, user)
            return redirect("homepage")

    else:
        form = UserSignInForm()
    return render(request, "user/signin_page.html", {'form':form})

def logout(request):
    ''' LOG OUT USER
        Remove all information about user from session, then user can sign in or registration again'''

    storage = messages.get_messages(request)
    storage.usage = True
    try:
        del request.session['user_role']
        del request.session["user_login"]
        del request.session['user_name']
        del request.session['user_lastname']
        del request.session['user_mobile']
    except KeyError:
        return redirect("homepage")
    return redirect("homepage")

def render_comics(request, comics_title):
    comics_item = COMICS.objects.filter(comics_t = comics_title)
    query = f"SELECT author_id, author_name, author_lastname FROM comics_author_inf WHERE title = '{comics_title}';"
    authors = AUTHOR.objects.raw(query)
    query = f"SELECT publisher_id, publisher_name, about_pub FROM comics_publisher_inf WHERE title = '{comics_title}';"
    publisher = PUBLISHER.objects.raw(query)
    return render(request, "comics_page.html", {'comics_item':comics_item, 'authors':authors, 'publisher':publisher})

def render_author(request,comics_title, author_id):
    query = f"SELECT author_id, author_name, author_lastname, author_birth, about_author FROM author WHERE author_id = {author_id};"
    author = AUTHOR.objects.raw(query)
    return render(request, 'author_page.html',{"author":author})

def render_publisher(request, comics_title, publisher_id):
    query = f"SELECT publisher_id, publisher_name, about_pub FROM comics_publisher_inf WHERE title = '{comics_title}';"
    publisher = PUBLISHER.objects.raw(query)
    return render(request, "publisher_page.html", {"publisher": publisher})

def do_order(request, comics_title):
    storage = messages.get_messages(request)
    storage.usage = True
    if('user_login' not in request.session) :
        messages.success(request, "Sorry you must sign in or register")
        return redirect("comics_render",comics_title)
    comics = COMICS.objects.get(comics_t = comics_title)

    if (comics.comics_amount <= 0 ):
        messages.success(request, "Sorry now you can't purchase this comics. Сomics not available")
        return redirect("comics_render", comics_title)

    if (request.method == 'POST'):
        form = OrderForm(request.POST)
        if (form.is_valid()):
            user_name = form.cleaned_data['name']
            user_lastname = form.cleaned_data['lastname']
            mob = form.cleaned_data['user_mobile']
            address = form.cleaned_data['user_address']
            login = request.session['user_login']
            cursor = connections['default'].cursor()
            cursor.execute(f'CALL insert_order("{login}", current_date(), "{address}",{comics.comics_id}, "{user_name}","{user_lastname}", "{mob}", 1);')
            return redirect("homepage")

    else :
        # user_name = request.session['user-name']
        # user_lastname = request.session['user_lastname']
        messages.success(request, "if you want you can cange the purchaser")
        form = OrderForm(initial={"name":request.session['user_name'], "lastname":request.session['user_lastname'], "user_mobile":request.session['user_mobile']})
    return render(request,"order/order_page.html", {'form':form, 'comics_t':comics_title})


def order_history(request):
    if ('user_login' in request.session):
        user = USER.objects.get(user_login = request.session['user_login'])
        order_item = ORDER_HISTORY.objects.filter(user_id = user.user_id).select_related()
        return render(request, "order/order_history_page.html", {"user_id":user.user_id, "order_item":order_item})
    return redirect('homepage')

def profile(request):
    if ('user_login' not in request.session):
        return redirect("homepage")
    print(request.session['user_login'])
    user = USER.objects.get(user_login = request.session['user_login'])
    return render(request, "user/profile.html", {"user":user})

def edit_profile(request):
    storage = messages.get_messages(request)
    storage.usage = True
    if ('user_login' not in request.session):
        return redirect("homepage")

    if (request.method == 'POST'):

        form = UserInfForm(request.POST)
        if (form.is_valid()):
            params = GetUserInfFromForm(form)
            old_login = request.session['user_login']
            cursor = connections['default'].cursor()
            cursor.callproc("update_user",[old_login] + params )
            request.session['user_login'] = params[2]
            request.session['user_name'] = params[0].capitalize()
            request.session['user_lastname'] = params[1].capitalize()
            request.session['user_mobile'] = params[4]
            messages.success(request, "You edit your profile information")
            return redirect("homepage")
    else :
        user = USER.objects.get(user_login = request.session["user_login"])
        form = UserInfForm(initial={'name':user.user_name, 'lastname':user.user_lastname, 'login':user.user_login, 'email':user.user_email, 'mobile': user.user_mobile, })
    return render(request, "user/edit_profile.html", {'form':form})

def all_comics_render(request):
    comicses = COMICS.objects.all()
    return render(request, "all_comics.html", {'comics_item': comicses})

def delete_item(request, _code_, name):
    storage = messages.get_messages(request)
    storage.usage = True
    if (_code_ == 1):
        comics = COMICS.objects.get(comics_t = name)
        # print(os.path.join(settings.BASE_DIR ,"static",comics.path_image.replace('/','\\').split('\\',1)[1]))
        os.remove(os.path.join(settings.BASE_DIR ,"static",comics.path_image.replace('/','\\').split('\\',1)[1]))
        cursor = connections['default'].cursor()
        cursor.execute(f"CALL delete_comics({comics.comics_id});")
        messages.success(request, f"Comics {name} is deleted")
        return redirect("all_comics")
    if(_code_  == 2):
        author = AUTHOR.objects.get(author_id = int(name))
        cursor = connections['default'].cursor()
        cursor.execute(f"CALL delete_author({author.author_id});")
        return redirect("authors")
    if(_code_ == 3):
        pub = PUBLISHER.objects.get(publisher_name=name)
        cursor = connections['default'].cursor()
        cursor.execute(f"CALL delete_publisher({pub.publisher_id});")
        return redirect("publishers")

def publishers(request):
    publishers = PUBLISHER.objects.all()
    return render(request, "all_publisher.html", {"publishers":publishers})

def search_author(request):
    if (request.method == "POST"):
        authors = None
        search_data = request.POST["search-data"]
        if(search_data):
            authors = AUTHOR.objects.filter(Q(author_name__startswith = search_data.capitalize()) | Q(author_lastname__startswith = search_data.capitalize()))
        return render(request, "search_author.html", {"authors":authors})
    else:
        return render(request, "search_comics.html", {"authors":authors})

def only_author(request, id):
    author = AUTHOR.objects.filter(author_id = id)
    return render(request, 'author_page.html',{"author":author})

def authors(request):
    authors = AUTHOR.objects.all()
    return render(request, "authors.html", {'authors':authors})

def only_publisher(request, id):
    publisher = PUBLISHER.objects.filter(publisher_id=id)
    return render(request, "publisher_page.html", {'publisher':publisher})

def add_comics(request):
    storage = messages.get_messages(request)
    storage.usage = True
    if (request.method == "POST"):
        form = NewComicsForm(request.POST, request.FILES)
        if (form.is_valid()and ("comics_image" in request.FILES)):
            title = form.cleaned_data["title"]
            date_public = form.cleaned_data["date_public"]
            about = form.cleaned_data["about"]
            price = form.cleaned_data["price"]
            amount = form.cleaned_data["amount"]
            comics_image = request.FILES["comics_image"]
            publisher = form.cleaned_data["publisher"]
            author = form.cleaned_data["author"]
            fs = FileSystemStorage(location = "E:\coursework\comics_site\static\comics_images" )
            file = fs.save(comics_image.name, comics_image)
            file_url = fs.url(file)
            cursor = connections['default'].cursor()
            args = [title, "/comics_images/" + file, about, date_public, price, publisher.publisher_id, amount]
            cursor.callproc("insert_comics",args)
            comics = COMICS.objects.get(comics_t__iexact=title)
            for auth in author:
                 cursor.execute(f"CALL insert_comics_author({comics.comics_id}, {auth.author_id} )")
            messages.success(request,f"{comics.comics_t} added")
            return redirect("add_comics")
    else:
        form = NewComicsForm()
    return render(request, "adminSpace/add_comics.html", {'form':form})

def add_publisher(request):
    storage = messages.get_messages(request)
    storage.usage = True
    if (request.method == "POST"):
        form = NewPublisherForm(request.POST)
        if (form.is_valid()):
            name = form.cleaned_data['name']
            about = form.cleaned_data['about']
            cursor = connections['default'].cursor()
            cursor.execute(f"CALL insert_publisher('{name}', '{about}');")
            messages.success(request, f"Publisher {name.capitalize()} added")

    else:
        form = NewPublisherForm()
    return render(request, "adminSpace/add_publisher.html", {"form":form})

def add_author(request):
    storage = messages.get_messages(request)
    storage.usage = True
    if (request.method  == "POST"):
        form = NewAuthorForm(request.POST)
        if (form.is_valid()):
            name = form.cleaned_data["name"]
            lastname = form.cleaned_data["lastname"]
            birth = form.cleaned_data["birth"]
            about = form.cleaned_data["about"]
            cursor = connections['default'].cursor()
            cursor.callproc("insert_author", [name,lastname,about,birth])
            messages.success(request, f"{name.capitalize()} {lastname.capitalize()} added")
    else :
        form = NewAuthorForm()
    return render(request, "adminSpace/add_author.html",{"form":form})

def edit_comics(request, id):
    storage = messages.get_messages(request)
    storage.usage = True
    if (request.method == "POST"):
        form = EditComicsForm(request.POST)
        if (form.is_valid()):
            title = form.cleaned_data["title"]
            date_public = form.cleaned_data["date_public"]
            about = form.cleaned_data["about"]
            price = form.cleaned_data["price"]
            amount = form.cleaned_data["amount"]
            comics = COMICS.objects.filter(comics_t__iexact = title).first()
            if (comics) and (comics.comics_id != id ):
                messages.success(request,f"{title} this comics already exists")
            else :
                cursor = connections['default'].cursor()
                cursor.callproc("update_comics",[id, title, about, date_public, price, amount])
                messages.success(request,f"{title.upper()} edited")
                return redirect("edit_comics", id)
    else:
        comics = COMICS.objects.get(comics_id = id)
        form = EditComicsForm(initial={'title': comics.comics_t, 'about': comics.about_comics, 'price':comics.comics_price, 'date_public':comics.date_public, "amount": comics.comics_amount})
    return render(request, "adminSpace/edit_comics.html", {'form':form})

def edit_author(request, id ):
    storage = messages.get_messages(request)
    storage.usage = True
    if (request.method  == "POST"):
        form = EditAuthorForm(request.POST)
        if (form.is_valid()):
            name = form.cleaned_data["name"]
            lastname = form.cleaned_data["lastname"]
            birth = form.cleaned_data["birth"]
            about = form.cleaned_data["about"]

            cursor = connections['default'].cursor()
            cursor.callproc("update_author", [id, name, lastname, about, birth])
            messages.success(request, f"{name.capitalize()} {lastname.capitalize()} are edited")
        return redirect("edit_author", id)
    else :
        author = AUTHOR.objects.get(author_id = id)
        form = EditAuthorForm(initial={'name': author.author_name, 'lastname':author.author_lastname, 'about':author.about, 'birth':author.author_birth})
    return render(request, "adminSpace/edit_author.html",{"form":form})

def edit_publisher(request, id ):
    storage = messages.get_messages(request)
    storage.usage = True
    if (request.method == "POST"):
        form = EditPublisherForm(request.POST)
        if (form.is_valid()):
            name = form.cleaned_data['name']
            about = form.cleaned_data['about']
            publ = PUBLISHER.objects.filter(publisher_name__iexact = name).first()
            if (publ) and ( publ.publisher_id != id ):
                messages.success(request, f"Publisher {name.capitalize()} already exists")
            cursor = connections['default'].cursor()
            cursor.callproc("update_publisher", [id, name, about])
            messages.success(request, f"Publisher {name.capitalize()} edited")
        return redirect("edit_publisher", id)
    else:
        pub = PUBLISHER.objects.get(publisher_id = id )
        form = EditPublisherForm(initial={'name': pub.publisher_name, 'about':pub.about_pub})
    return render(request, "adminSpace/edit_publisher.html", {"form":form})

def see_orderline(request):
    order_line = ORDER_LINE.objects.filter(~Q(status_id = 2), ~Q(status_id = 3)).select_related()
    return render(request, "order/order_line.html", {'order_line':order_line})

def manage_order_line(request, id):
    storage = messages.get_messages(request)
    storage.usage = True
    order_item = ORDER_HISTORY.objects.select_related().get(order_id = id)
    if (request.method == "POST"):
        form = ManageOrderForm(request.POST)
        if (form.is_valid()):
            status = form.cleaned_data['status']
            comment = request.POST['comment']
            cursor = connections['default'].cursor()
            cursor.callproc("update_status_order", [order_item.order_id.order_id, status.status_id])
            if (comment != ""):
                cursor.execute(f"update order_history set coment = '{comment}' where history_id = {order_item.history_id} ; ")
            return redirect("see_orderline")
    else :
        form = ManageOrderForm()
    return render(request, "adminSpace/manage_order.html", {"order_item":order_item.order_id, "form":form})
