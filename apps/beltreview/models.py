from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register(self, name, alias, email, password, conpass):
        errors = []
        the_user = User.objects.filter(email = email)
        if len(name) < 1:
            errors.append('Name is too short')
        if len(alias) < 1:
            errors.append('Alias is too short')
        if not EMAIL_REGEX.match(email):
            errors.append('Invalid Email')
        if the_user:
            errors.append('Already in system')
        if len(password) < 5:
            errors.append('Name is too short')
        if conpass != password:
            errors.append('Passwords don\'t match')
        if len(errors) > 0:
            return errors
        else:
            return True

    def login(self, email, password):
        errors = []
        the_user = User.objects.filter(email = email)
        if the_user:
            if bcrypt.hashpw(password.encode('utf-8'), the_user[0].password.encode('utf-8')) == the_user[0].password:
                #needed help from other assignment
                return True
            else:
                errors.append('Wrong Email or Password')
                return errors
        else:
            errors.append('Wrong Email or Password')
            return errors


class User(models.Model):
    name = models.CharField(max_length = 200)
    alias = models.CharField(max_length = 200)
    email = models.CharField(max_length = 200)
    password = models.CharField(max_length = 200)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Book(models.Model):
    book = models.CharField(max_length = 200)
    author = models.CharField(max_length = 200, default = '')


class Review(models.Model):
    book = models.ForeignKey(Book)
    name = models.ForeignKey(User)
    rating = models.IntegerField(default = 0)
    review = models.TextField(max_length = 1000)
