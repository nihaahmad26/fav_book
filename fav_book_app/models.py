from django.db import models
from datetime import datetime
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        check = User.objects.filter(email = postData['email'])
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name has to be at least 2 characters long."
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name has to be at least 2 characters long."
        if len(postData['password']) < 8:
            errors['password'] = "Passwords must be atleast 8 characters long"
        elif postData['password'] != postData['confirm_password']:
            errors['password'] = "Passwords must match"
        if len(postData['email']) < 1:
            errors['reg_email'] = "Must enter an Email"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['reg_email'] = "Please enter a valid email address"
        elif check:
            errors['reg_email'] = "Email address is already in use"
        return errors

    def login_validator(self, postData):
        errors = {}
        check = User.objects.filter(email = postData['login_email'])
        if not check:
            errors['login_email'] = "email is not registered"
        else:
            if not bcrypt.checkpw(postData['login_password'].encode(), check[0].password.encode()):
                errors['login_email'] = "email and password do not match"
            return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()

class BookManager(models.Manager):
    def book_validator(self, postData):
        errors = {}
        if len(postData['title']) < 1:
            errors['title'] = "must have a title"
        if len(postData['description']) < 5:
            errors['description'] = "description must be atleast 5 characters long"
        return errors


class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name="has_created_books", on_delete=models.CASCADE)
    favorited_by = models.ManyToManyField(User, related_name="favorited_books")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = BookManager()


