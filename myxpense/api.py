from tastypie.resources import ModelResource
from tastypie import fields
from .models import *
from tastypie.authorization import Authorization
from tastypie.exceptions import ImmediateHttpResponse
from tastypie import http
from django.db.models import Q
from myxpense import expense_interactors, expense_paid_by_interactors
from myxpense import utils

class PersonResource(ModelResource):
    created_by = fields.CharField(null=True, blank=True)
    total_amount_person_has_to_pay = fields.FloatField()
    total_amount_person_has_to_get_paid = fields.FloatField()

    class Meta:
        queryset = User.objects.all()
        resource_name = 'person'
        excludes = ['is_staff', 'is_superuser', 'password']
        always_return_data = True
        authorization = Authorization()

    def dehydrate_total_amount_person_has_to_pay(self, bundle):
        return expense_interactors.total_amount_person_has_to_pay(bundle.obj.id)

    def dehydrate_total_amount_person_has_to_get_paid(self, bundle):
        return expense_interactors.total_amount_person_has_to_get_paid(bundle.obj.id)

    def hydrate_created_by(self, bundle):
        parent_id = int(bundle.data['created_by'].split('/')[-2])
        parent = User.objects.get(pk=parent_id)
        bundle.obj.save()
        UserProfile.objects.get_or_create(user=bundle.obj, parent=parent)
        return bundle

    def dehydrate_created_by(self, bundle):
        return u'/api/v1/person/{}/'.format(bundle.obj.userprofile.parent.id)

    def obj_create(self, bundle, **kwargs):
        if User.objects.filter(username=bundle.data.get('username')):
            raise ImmediateHttpResponse(response=http.HttpBadRequest('username already in use'))
        if User.objects.filter(email=bundle.data.get('email')):
            raise ImmediateHttpResponse(response=http.HttpBadRequest('email already in use'))
        return super(PersonResource, self).obj_create(
            bundle, **kwargs)

    def get_object_list(self, request):
        expense_books = ExpenseBook.objects.filter(people=request.user)
        return super(PersonResource, self).get_object_list(
            request).filter(
            Q(expensebook=expense_books) |
            Q(pk=request.user.id) |
            Q(userprofile__parent=request.user)
        ).distinct()

class ExpenseBookResource(ModelResource):
    people = fields.ToManyField(PersonResource, 'people', null=True)

    class Meta:
        queryset = ExpenseBook.objects.all()
        resource_name = 'expense_book'
        authorization = Authorization()
        always_return_data = True

    def get_object_list(self, request):
        return super(ExpenseBookResource, self).get_object_list(
            request).filter(people=request.user)


class ExpensePaidbyResource(ModelResource):
    person = fields.ToOneField(PersonResource, 'person')

    class Meta:
        queryset = ExpensePaidby.objects.all()
        resource_name = 'expense_paid_by'
        authorization = Authorization()
        always_return_data = True


class ExpenseResource(ModelResource):
    associated_with = fields.ToOneField(
        ExpenseBookResource, 'associated_with', full=True, null=True)
    paid_by = fields.ToManyField(
        ExpensePaidbyResource, 'paid_by', full=True, null=True)
    shared_with = fields.ToManyField(
        PersonResource, 'shared_with', full=True, null=True)

    class Meta:
        queryset = Expense.objects.all()
        resource_name = 'expense'
        authorization = Authorization()
        always_return_data = True

    def get_object_list(self, request):
        return super(ExpenseResource, self).get_object_list(
            request).filter(Q(paid_by__person=request.user) | Q(shared_with=request.user)).distinct()


    def obj_create(self, bundle, **kwargs):
        expense_name = bundle.data['expense_name']
        expense_type = bundle.data['expense_type']
        associated_with = utils.uri2obj(bundle.data['associated_with'])
        paid_by = expense_paid_by_interactors.create_expense_paid_by_list(bundle.data['paid_by'])
        shared_with = utils.urilist2objlist(bundle.data['shared_with'])
        expense = expense_interactors.create_expense(
            expense_type=expense_type,
            expense_name=expense_name,
            associated_with=associated_with,
            shared_with=shared_with,
            paid_by=paid_by)
        expense_interactors.compute_expenses(expense)
        bundle.obj = expense
        bundle.obj.save()
        return bundle
