import unittest

from myxpense import expense_book_interactors, expense_interactors, people_interactors, expense_paid_by_interactors


class MyXpenseTests(unittest.TestCase):
    def test_creation_of_people_and_creation_of_expense_book_and_expenses(self):
        person0 = people_interactors.create_person(
            name='Ram Lal', email='ram@lal.com')
        person1 = people_interactors.create_person(
            name='Bheem Lal', email='bheem@lal.com')
        person2 = people_interactors.create_person(
            name='Manish Lal', email='mansih@lal.com')
        person3 = people_interactors.create_person(
            name='Rahul Lal', email='rahul@lal.com')

        people = [person0, person1, person2, person3]
        title = 'My first expense book'
        description = 'a small description'
        currency = 'INR'

        expense_book = expense_book_interactors.create_expense_book(
            title=title,
            description=description,
            currency=currency,
            people=people
        )

        self.assertEqual(expense_book.title, title)
        self.assertEqual(expense_book.description, description)
        self.assertEqual(expense_book.currency, currency)
        self.assertEqual(list(expense_book.people.all()), people)


        expense_paid_by0 = expense_paid_by_interactors.create_expense_paid_by(person0, 25)

        expense_type = 'petrol'
        expense_name = 'petrol'
        expense = expense_interactors.create_expense(
            associated_with=expense_book,
            expense_type=expense_type,
            expense_name=expense_name,
            paid_by=[expense_paid_by0],
            shared_with=[people[1]],
        )

        self.assertEqual(expense.associated_with, expense_book)
        self.assertEqual(expense.expense_type, expense_type)
        self.assertEqual(expense.expense_name, expense_name)
        self.assertEqual(list(expense.paid_by.all()), [expense_paid_by0])
        self.assertEqual(list(expense.shared_with.all()), [people[1]])

        tracked_expenses = expense_interactors.compute_expenses(expense)
        self.assertEqual(len(tracked_expenses), 2)
        self.assertEqual(
            sum([trk_exp.how_much_to_pay for trk_exp in tracked_expenses]),
            0
        )

        expense_paid_by1 = expense_paid_by_interactors.create_expense_paid_by(person1, 5)
        tracked_expenses = expense_interactors.pay_back(expense, expense_paid_by1)
        self.assertEqual(len(tracked_expenses), 2)
        self.assertEqual(
            sum([trk_exp.how_much_to_pay for trk_exp in tracked_expenses]),
            7.5
        )

        expense_paid_by1 = expense_paid_by_interactors.create_expense_paid_by(person1, 7)
        tracked_expenses = expense_interactors.pay_back(expense, expense_paid_by1)
        self.assertEqual(len(tracked_expenses), 2)
        self.assertEqual(
            sum([trk_exp.how_much_to_pay for trk_exp in tracked_expenses]),
            0.5
        )

        expense_paid_by1 = expense_paid_by_interactors.create_expense_paid_by(person1, 0.5)
        tracked_expenses = expense_interactors.pay_back(expense, expense_paid_by1)
        self.assertEqual(len(tracked_expenses), 2)
        self.assertEqual(
            sum([trk_exp.how_much_to_pay for trk_exp in tracked_expenses]),
            0
        )

        expense_paid_by0 = expense_paid_by_interactors.create_expense_paid_by(person0, 150.22)
        expense_paid_by1 = expense_paid_by_interactors.create_expense_paid_by(person1, 60.75)
        expense_paid_by2 = expense_paid_by_interactors.create_expense_paid_by(person2, 25.5)

        expense_type = 'breakfast'
        expense_name = 'eating samosa & pakoda'

        expense = expense_interactors.create_expense(
            associated_with=expense_book,
            expense_type=expense_type,
            expense_name=expense_name,
            paid_by=[expense_paid_by0, expense_paid_by1, expense_paid_by2],
            shared_with=[people[1]],
        )

        expense_interactors.compute_expenses(expense)

        self.assertEqual(expense_interactors.total_amount_person_has_to_pay(person0), 0)
        self.assertEqual(expense_interactors.total_amount_person_has_to_pay(person1), 59.1175)
        self.assertEqual(expense_interactors.total_amount_person_has_to_pay(person2), 33.6175)
        self.assertEqual(expense_interactors.total_amount_person_has_to_pay(person3), 0)

        self.assertEqual(expense_interactors.total_amount_person_has_to_get_paid(person0), 91.10249999999999)
        self.assertEqual(expense_interactors.total_amount_person_has_to_get_paid(person1), 1.6325000000000003)
        self.assertEqual(expense_interactors.total_amount_person_has_to_get_paid(person2), 0)
        self.assertEqual(expense_interactors.total_amount_person_has_to_get_paid(person3), 0)

        self.assertEqual(expense_interactors.people_person_has_to_pay(person0), [])
        self.assertEqual(expense_interactors.people_person_has_to_pay(person1), [person1])
        self.assertEqual(expense_interactors.people_person_has_to_pay(person2), [person2])
        self.assertEqual(expense_interactors.people_person_has_to_pay(person3), [])

        self.assertEqual(expense_interactors.people_person_has_to_get_paid(person0), [person0])
        self.assertEqual(expense_interactors.people_person_has_to_get_paid(person1), [person1])
        self.assertEqual(expense_interactors.people_person_has_to_get_paid(person2), [])
        self.assertEqual(expense_interactors.people_person_has_to_get_paid(person3), [])


