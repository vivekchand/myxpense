from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.db.models import Q

from .models import ExpenseBook, Expense


def get_user(username_or_email):
    try:
        return User.objects.get(email=username_or_email)
    except User.DoesNotExist:
        try:
            return User.objects.get(username=username_or_email)
        except User.DoesNotExist:
            return None

def redirect_to_app_if_loggedn(func):
    def _wrapped_func(*args, **kwargs):
        request = args[0]
        if request.user.is_authenticated():
            return HttpResponseRedirect('/app/#/')
        return func(*args, **kwargs)

    return _wrapped_func


def login_required(func):
    def _wrapped_func(*args, **kwargs):
        request = args[0]
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login')
        return func(*args, **kwargs)

    return _wrapped_func

def get_or_create_user(email, name):
    user, created = User.objects.get_or_create(email=email, username=email)
    if name:
        user.first_name = name.split(' ')[0]
        if len(name.split(' '))>1:
            user.last_name = ' '.join(name.split(' ')[1:])
    user.save()
    return user

def get_name(user):
    if user.first_name and user.last_name:
        return "%s %s" % (user.first_name, user.last_name)
    elif user.first_name:
        return user.first_name
    else:
        return user.email.split('@')[0]

def get_expense_books(user):
    return ExpenseBook.objects.filter(people=user)

def get_expenses(user):
    return Expense.objects.filter(Q(paid_by__person=user) | Q(shared_with=user))

User.add_to_class('name', get_name)
User.add_to_class('expenses', get_expenses)
User.add_to_class('expense_books', get_expense_books)

def user_has_expense_books(user):
    expense_books = ExpenseBook.objects.filter(people=user)
    return expense_books.count()>0

def get_total_amount(amounts):
    total_amount = 0
    for amount in amounts:
        total_amount += float(amount)
    return total_amount

