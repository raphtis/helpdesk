from django.db import models
import re
import bcrypt

# Create your models here.
class TicketManager(models.Manager):
    def ticket_validator(self, postData):
        errors = {}
        if len(postData['subject']) < 2:
            errors ['subject'] = "Subject name is too short."
        if len(postData['ticket_type']) < 1:
            errors ['ticket_type'] = "Must select a ticket type."
        if len(postData['ticket_status']) < 1:
            errors ['ticket_status'] = "Must select a ticket status."
        if len(postData['ticket_description']) < 10:
            errors ['ticket_description'] = "Description must be 10 characters or longer."
        return errors


class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be 2 characters or more."

        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be 2 characters or more."

        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['email'])==0:
            errors['email'] = "You must enter an email"
        elif not email_regex.match(postData['email']):
            errors['email'] = "Must be a valid email"

        current_users = User.objects.filter(email=postData['email'])
        if len(current_users) > 0:
            errors['duplicate'] = "That email is already in use"
        

        if len(postData['password']) < 8:
            errors["password"] = "Password must be 8 characters or more."

        if postData['password'] != postData['confirm_password']:
            errors["match"] = "Passwords do not match."

        return errors

    def login_validator(self, postData):
        errors = {}
        existing_user = User.objects.filter(email=postData['email'])
        if len(postData['email']) == 0:
            errors['email'] = "Email must be entered."

        if len(postData['password']) < 8:
            errors['password'] = "Password must be 8 characters or more."
        
        elif bcrypt.checkpw(postData['password'].encode(), existing_user[0].password.encode()) != True:
            errors['password'] = "Email and password do not match."
        
        return errors



class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
class Ticket(models.Model):
    subject = models.CharField(max_length=250)
    ticket_type = models.CharField(max_length=50)
    ticket_status = models.CharField(max_length=50)
    ticket_description = models.CharField(max_length=350)
    created_by = models.ForeignKey(User, related_name="user_tickets", on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TicketManager()
    
class Comment(models.Model):
    comment = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, related_name="post_comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
