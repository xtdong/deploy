from __future__ import unicode_literals
from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import bcrypt


class UsersManager(models.Manager):
    def check_registration_data(self, postData):
        errors = {}

        if len(postData['first_name']) < 3:
            errors["first_name"] = "First Name Too short"

        if len(postData['last_name']) < 3:
            errors["last_name"] = "Last Name Too short"

        existing_users = Users.objects.filter(email=postData['email'])
        if existing_users:
            errors['email2'] = "The email has been registered"

        # Check if the email is a valid email formatted string
        # E.g., a@a.com
        try:
            validate_email(postData['email'])
        except ValidationError:
            errors["email1"] = "Email is invalid"

        if len(postData['password']) < 2:
            errors["password_length"] = "Password is too short"

        if postData['password'] != postData['password_confirmation']:
            errors["password_match"] = "Passwords are not matching"

        return errors


class Users(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(max_length=45)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UsersManager()


class Books(models.Model):
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    user = models.ForeignKey(
        'Users', on_delete=models.CASCADE, related_name='books')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Reviews(models.Model):
    text = models.TextField()
    rating = models.IntegerField()
    user = models.ForeignKey(
        'Users', on_delete=models.CASCADE, related_name='reviews')
    book = models.ForeignKey(
        'Books', on_delete=models.CASCADE, related_name='reviews')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
