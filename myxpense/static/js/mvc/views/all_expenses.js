var app = app || {};

app.ExpenseRowView = Backbone.View.extend({
    tagName: 'tr',
	template: _.template( $('#jst-expense-row').html() ),

	render: function(){
        var data = this.model.toJSON();
        var paid_by_list = [];
        for( var i=0; i<data.paid_by.length; i++ ){
            paid_by_list.push({'username': app.people.get(data.paid_by[i].person).get('username'),
                                'amount': data.paid_by[i].amount
                            });
        }
        data.paid_by_list = paid_by_list;
        this.$el.html( this.template( data ) );
        return this;
	}

});

app.AllExpensesView = Backbone.View.extend({
	el: '#js-expense-row',

    initialize: function() {
        this.render();
        this.listenTo(app.expenses, 'reset', this.render);
    },

    render: function() {
        app.expenses.each(function(item) {
            this.renderExpense(item);
        }, this);
    },


    renderExpense: function(item){
    	var expenseRowView = new app.ExpenseRowView({
    		model: item
    	});
    	this.$el.append( expenseRowView.render().el );

    }

});
