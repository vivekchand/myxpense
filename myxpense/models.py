from django.db import models
from django.contrib.auth.models import User
from django.db.models import DO_NOTHING


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="userprofile")
    parent = models.ForeignKey(User, related_name="children_set",
                               on_delete=DO_NOTHING)

class ExpenseBook(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    currency = models.CharField(max_length=100)
    people = models.ManyToManyField(User, blank=True, null=True)


class ExpensePaidby(models.Model):
    person = models.ForeignKey(
        User, related_name="person", blank=True, null=True)
    amount = models.FloatField(default=0.0)


class Expense(models.Model):
    associated_with = models.ForeignKey(
        ExpenseBook, related_name="expense", blank=True, null=True)
    expense_type = models.CharField(max_length=100)
    expense_name = models.CharField(max_length=200)
    paid_by = models.ManyToManyField(ExpensePaidby, blank=True, null=True)
    shared_with = models.ManyToManyField(User, blank=True, null=True)



class ExpenseTracker(models.Model):
    person = models.ForeignKey(User, blank=True, null=True)
    how_much_to_pay = models.FloatField(null=True, default=0.0)
    expense = models.ForeignKey(Expense, blank=True, null=True)
