from django.contrib.auth.models import User
from myxpense.models import Expense, ExpenseBook, ExpensePaidby


def uri2obj(uri):
    type = uri.split('/')[3]
    id = uri.split('/')[4]
    if type == 'expense':
        return Expense.objects.get(pk=id)
    if type == 'expense_book':
        return ExpenseBook.objects.get(pk=id)
    if type == 'person':
        return User.objects.get(pk=id)
    if type == 'expense_paid_by':
        return ExpensePaidby.objects.get(pk=id)


def urilist2objlist(urilist):
    return [uri2obj(uri) for uri in urilist]
