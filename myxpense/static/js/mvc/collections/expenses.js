var app = app || {};

app.Expenses = Backbone.Collection.extend({
    model: app.Expense,
    url: '/api/v1/expense/'
});