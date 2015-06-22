var app = app || {};

app.ExpenseBookRowView = Backbone.View.extend({
    tagName: 'tr',
    template: _.template( $('#jst-expense-book-row').html() ),

    render: function(){
        var data = this.model.toJSON();
        var people = [];
        for( var i=0; i<data.people.length; i++ ){
            people.push(app.people.get(data.people[i]).get('username'));
        }
        data.people = people
        this.$el.html( this.template( data ) );
        return this;
    }

});


app.AllExpenseBooksView = Backbone.View.extend({
    el: '#js-expense-book-row',

    initialize: function() {
        this.render();
        this.listenTo(app.expense_books, 'reset', this.render);
    },


    render: function() {
        app.expense_books.each(function(item) {
            this.renderExpenseBook(item);
        }, this);
    },


    renderExpenseBook: function(item){
        var expenseBookRowView = new app.ExpenseBookRowView({
            model: item
        });
        this.$el.append( expenseBookRowView.render().el );

    }

});
