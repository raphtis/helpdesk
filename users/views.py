from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import time
import bcrypt


# Create your views here.
def index(request):
    return render(request, "index.html")

# REGISTER
def register(request): 
    if request.method == "POST":
        errors = User.objects.reg_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/new_user')

        # hash the password!!!!
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        # create a new user
        new_user = User.objects.create(
            first_name = request.POST['first_name'], 
            last_name = request.POST['last_name'], 
            email = request.POST ['email'], 
            password = hashed_pw
        )
        # create a new session
        request.session['user_id'] = new_user.id
        return redirect ('/profile')
    
#REG PAGE
def new_user(request):
    return render(request, 'register.html')

#USER PROFILE
def profile(request):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.filter(id = request.session['user_id'])
    context = {
        'user': this_user[0],
        'all_tickets': Ticket.objects.all(),
        'all_comments': Comment.objects.all()
    }
    return render(request, 'profile.html', context)

# LOG IN
def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        this_user = User.objects.filter(email = request.POST['email'])
        request.session['user_id'] = this_user[0].id
        return redirect('/dashboard')
    return redirect('/')

# LOG OUT
def logout(request):
    request.session.flush()
    return redirect('/')

# USER
def update_user(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/')
    errors = User.objects.reg_validator(request.POST)
    if errors: 
        for val in errors.values():
            messages.errors(request, val)
    else: 
        user = User.objects.get(id=request.session['user_id'])
        new_user = User.objects.get(id=user_id)
        new_user.first_name = request.POST['first_name']
        new_user.last_name = request.POST['last_name']
        new_user.email = request.POST['email']
        new_user.save()
        messages.success(request, "User profile successfully updated.")
    return redirect('/profile')

#TICKET DASHBOARD
def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'all_tickets': Ticket.objects.all()
    }
    return render(request, 'dashboard.html', context)


#CREATE TICKET
def create_ticket(request):
    if 'user_id' not in request.session:
        return redirect('/')
    errors = Ticket.objects.ticket_validator(request.POST)
    if errors:
        for val in errors.values():
            messages.error(request, val)
        return redirect('/ticket_form')
    else:
        
        Ticket.objects.create(
            subject = request.POST['subject'],
            ticket_type = request.POST['ticket_type'],
            ticket_status = request.POST['ticket_status'],
            ticket_description = request.POST['ticket_description'],
            created_by = User.objects.get(id=request.session['user_id'])
        )
        messages.success(request, "Ticket successfully created.")
    return redirect('/dashboard')


# ADD TICKET FORM
def ticket_form(request):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.filter(id = request.session['user_id'])
    context = {
        'user': this_user[0]
    }
    return render(request, 'create-ticket.html', context)

#EDIT TICKET
def edit_ticket(request, ticket_id):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        "ticket": Ticket.objects.get(id=ticket_id)
    }
    return render(request, "ticket-details.html", context)

#UPDATE TICKET 
def update_ticket(request, ticket_id):
    if 'user_id' not in request.session:
        return redirect('/')
    errors = Ticket.objects.ticket_validator(request.POST)
    if errors:
        for val in errors.values():
            messages.error(request, val)

    else: 
        user = User.objects.get(id=request.session['user_id'])
        new_ticket = Ticket.objects.get(id=ticket_id)
        new_ticket.subject = request.POST['subject']
        new_ticket.ticket_type = request.POST['ticket_type']
        new_ticket.ticket_status = request.POST['ticket_status']
        new_ticket.ticket_description = request.POST['ticket_description']
        new_ticket.save()
        messages.success(request, "Ticket has been successfully updated.")
    return redirect('/dashboard')

def delete_ticket(request, ticket_id):
    if 'user_id' not in request.session:
        return redirect('/')
    to_delete = Ticket.objects.get(id=ticket_id)
    to_delete.delete()
    messages.success(request, "Ticket removed from list.")
    return redirect('/dashboard')


def add_comment(request, ticket_id):
    poster = User.objects.get(id=request.session['user_id'])
    ticket = Ticket.objects.get(id=ticket_id)
    Comment.objects.create(comment=request.POST['comment'], poster=poster, ticket=ticket)
    return redirect('/success')

def success(request):
    return render(request, 'success.html')