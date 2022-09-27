from .models import  *

def GetUserInfFromForm(form):
    params = list()
    params.append(form.cleaned_data['name'])
    params.append(form.cleaned_data['lastname'])
    params.append(form.cleaned_data['login'])
    params.append(form.cleaned_data['email'])
    params.append(form.cleaned_data['mobile'])
    params.append(form.cleaned_data['password_2'])
    return params

def MapFormToUser(form):
    user = USER()
    user.user_name = form.cleaned_data['name']
    user.user_lastname = form.cleaned_data["lastname"]
    user.user_login = form.cleaned_data["login"]
    user.password = form.cleaned_data["password_2"]
    user.user_mobile = form.cleaned_data["mobile"]
    user.user_email = form.cleaned_data["email"]
    return user

def MapSignFormToUser(form):
    user = USER.objects.get(user_login = form.cleaned_data['login'])
    return user

def SetUserInSession(request, user):
    role = USER_ROLES.objects.get(user_id = user.user_id)
    request.session['user_login'] = user.user_login  # set user login in a session
    request.session['user_role'] = role.role_id # set user role on a session
    request.session['user_name'] = user.user_name # set user name
    request.session['user_lastname'] = user.user_lastname # set user lastname
    request.session['user_mobile'] = user.user_mobile
