from myxpense import utils
from myxpense.models import ExpensePaidby


def create_expense_paid_by(person, amount_paid):
    return ExpensePaidby.objects.create(
        person=person, amount=(amount_paid*1.0))

def create_expense_paid_by_list(expense_paid_by_list):
    return_list = []
    for expense_paid_by in expense_paid_by_list:
        exp_paid_by = ExpensePaidby.objects.create(
            person=utils.uri2obj(expense_paid_by['person']),
            amount=float(expense_paid_by['amount'])
        )
        return_list.append(exp_paid_by)
    return return_list