from myxpense.models import Expense, ExpenseTracker
from myxpense.people_interactors import get_people_related_to_person


def create_expense(
        associated_with, expense_type,
        expense_name, paid_by, shared_with):
    expense = Expense.objects.create(
        associated_with=associated_with, expense_type=expense_type,
        expense_name=expense_name)
    [expense.paid_by.add(person) for person in paid_by]
    [expense.shared_with.add(person) for person in shared_with]
    return expense

def compute_expenses(expense):
    expenses_paid_by = expense.paid_by.all()
    expenses_shared_with = expense.shared_with.all()
    total_people_involved = len(expenses_paid_by) + len(expenses_shared_with)
    total_amount = sum([exp_paid.amount for exp_paid in expenses_paid_by])
    divided_amount = total_amount / (total_people_involved * 1.0)

    tracked_expenses = []
    for exp_paid in expenses_paid_by:
        exp_track = ExpenseTracker.objects.create(
            person=exp_paid.person,
            how_much_to_pay=(divided_amount - exp_paid.amount),
            expense=expense
        )
        tracked_expenses.append(exp_track)

    for shared_with in expenses_shared_with:
        exp_track = ExpenseTracker.objects.create(
            person=shared_with,
            how_much_to_pay=divided_amount,
            expense=expense
        )
        tracked_expenses.append(exp_track)
    return tracked_expenses

def pay_back(expense, expense_paid_by):
    tracked_expenses = ExpenseTracker.objects.filter(expense=expense)

    for track_exp in tracked_expenses:
        if track_exp.person == expense_paid_by.person:
            track_exp.how_much_to_pay -= expense_paid_by.amount
            track_exp.save()

    paid_by_list = [track_exp for track_exp in tracked_expenses if track_exp.how_much_to_pay < 0]
    if not paid_by_list:
        return tracked_expenses

    total_paid_by = len(paid_by_list)
    divided_amount = expense_paid_by.amount / (total_paid_by * 1.0)

    for paid_by in paid_by_list:
        if paid_by.how_much_to_pay < divided_amount:
            divided_amount += (paid_by.how_much_to_pay - divided_amount)
            paid_by.how_much_to_pay = 0
            paid_by.save()
        else:
            paid_by.how_much_to_pay += divided_amount
            paid_by.save()
    return tracked_expenses

def total_amount_person_has_to_pay(person):
    return sum([how_much_to_pay for how_much_to_pay in ExpenseTracker.objects.filter(
        person=person).values_list(
        'how_much_to_pay', flat=True) if how_much_to_pay > 0])

def total_amount_person_has_to_get_paid(person):
    return sum([-how_much_to_pay for how_much_to_pay in ExpenseTracker.objects.filter(
        person=person).values_list(
        'how_much_to_pay', flat=True) if how_much_to_pay < 0])


#
# This is not the right way to compute
# def people_person_has_to_pay(person):
#     return list(set([et.person for et in ExpenseTracker.objects.filter(
#         person=person) if et.how_much_to_pay > 0]))
#
# def people_person_has_to_get_paid(person):
#     return list(set([et.person for et in ExpenseTracker.objects.filter(
#         person=person) if et.how_much_to_pay < 0]))


def update_expense():
    pass

def delete_expense():
    pass



