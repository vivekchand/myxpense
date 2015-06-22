var app = app || {};

app.ExpenseBooks = Backbone.Collection.extend({
    model: app.ExpenseBook,
    url: '/api/v1/expense_book/',
});