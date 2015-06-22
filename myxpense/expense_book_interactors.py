from .models import ExpenseBook

_sentinel = object()

def create_expense_book(title, description, currency, people):
    expense_book = ExpenseBook.objects.create(
        title=title,
        description=description,
        currency=currency,
    )
    [expense_book.people.add(person) for person in people]
    return expense_book

def update_expense_book(
        expense_book, title=_sentinel,
        description=_sentinel, currency=_sentinel):
    expense_book.title = title
    expense_book.description = description
    expense_book.currency = currency
    expense_book.save()

def delete_expense_book(expense_book):
    expense_book.delete()

def add_person_to_expense_book(expense_book, person):
    expense_book.people.add(person)

