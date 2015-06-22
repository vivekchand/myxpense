from django.contrib.auth.models import User
from django.db.models import Q
from myxpense.models import UserProfile, ExpenseBook


def create_person(name, email):
    user = User.objects.create(username=name, email=email)
    UserProfile.objects.create(user=user, parent=user)
    return user

def update_person(person, name, email):
    person.username = name
    person.email = email
    person.save()

def delete_person(person):
    person.delete()

def get_people_related_to_person(user):
    expense_books = ExpenseBook.objects.filter(people=user)
    return User.objects.filter(
        Q(expensebook=expense_books) |
        Q(pk=user.id) |
        Q(userprofile__parent=user)
    ).distinct()
