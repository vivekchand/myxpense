var app = app || {};

app.people = new app.People();
app.people.fetch({
    reset: true,
    async: false
});

app.expense_books = new app.ExpenseBooks();
app.expense_books.fetch({
    reset: true,
    async: false
});

app.expenses = new app.Expenses();
app.expenses.fetch({
    reset: true,
    async: false
});

app.Router = Backbone.Router.extend({
    routes: {
        "create_expense_book": 'create_expense_book',
        "add_expense": 'add_expense',
        "add_person": 'add_person',

        'all_expense_books': "all_expense_books",
        'all_expenses': "all_expenses",
        "all_people": "all_people",
        "": "dashboard"
    },

    templates: {
        create_expense_book: _.template( $('#jst-create-expense-book').html() ),
        add_expense: _.template( $('#jst-add-expense').html() ),
        add_person: _.template( $('#jst-add-person').html() ),
        all_expense_books: _.template( $('#jst-all-expense-books').html() ),
        all_expenses: _.template( $('#jst-all-expenses').html() ),
        all_people: _.template( $('#jst-all-people').html() ),
        dashboard: _.template( $('#jst-dashboard').html() )
    },

    initialize: function(){

    },

    create_expense_book: function() {
        $('#page-content').html( this.templates.create_expense_book );
        console.log('Create a expense book');
        new app.CreateExpenseBookView();
    },

    add_expense: function() {
        console.log('add expense');
        $('#page-content').html( this.templates.add_expense );
        new app.AddExpenseView();
    },

    add_person: function() {
        console.log('add person')
        $('#page-content').html( this.templates.add_person );
        new app.AddPersonView();
    },

    all_expense_books: function() {
        console.log('all expense books')
        $('#page-content').html( this.templates.all_expense_books );
        new app.AllExpenseBooksView();
    },

    all_expenses: function() {
        console.log('all expenses')
        $('#page-content').html( this.templates.all_expenses );
        new app.AllExpensesView();
    },

    all_people: function() {
        console.log('all people')
        $('#page-content').html( this.templates.all_people );
        new app.AllPeopleView();
    },

    dashboard: function() {
        console.log('dashboard')
        $('#page-content').html( this.templates.dashboard );
        new app.DashboardView();
    }

});
app.myrouter = new app.Router();
Backbone.history.start();
