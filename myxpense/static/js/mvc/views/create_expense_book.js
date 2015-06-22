var app = app || {};

app.CreateExpenseBookView = Backbone.View.extend({
	el: '#js_create_expense_book_form',

	templates: {
		people_list: _.template( $('#jst-people-list').html() )
	},

	events: {
		'click #js-create-expense-book': 'createExpenseBook',
		'click #js-add-person': 'addPerson',
	},

	initialize: function(){
		this.renderPeopleList();
		this.listenTo( app.people, 'add', this.renderPeopleList );
		this.listenTo( app.people, 'reset', this.renderPeopleList );
		this.model = new app.ExpenseBook({}, {
			collection: app.expense_books
		});		
	},

	renderPeopleList: function(){
		this.$('#js-people-list').html(
			this.templates.people_list(
				{'people': app.people.toJSON()}
				));		
	},

	addPerson: function(){
		var modalView = new app.AddPersonModalView();
		modalView.show();
	},

	createExpenseBook: function( e ){
		e.preventDefault();
		this.renderPeopleList();
		var arr = $('#js-people-list input:checked');
		var people = [];
		for(var i=0; i<arr.length; i++){
			people.push(arr[i].value);
		}
		var title = $('#js-title').val();
		var description = $('#js-description').val();
		var currency = $('#js-currency').val();
		var formData = { 'title':title, 
						 'description':description, 
						 'currency':currency,
						 'people': people };
		console.log('Create an expense book!!!!');
		this.model.save(formData, {
			success: function(model, response, options){
				app.expense_books.add(model);
				app.expense_books.fetch({reset: true, async: false});
				app.myrouter.navigate('/all_expense_books', true);
			},
			error: function(model, response, options){
				if(options.xhr.status == 201){
					app.expense_books.add(model);
					app.expense_books.fetch({reset: true, async: false});
					app.myrouter.navigate('/all_expense_books', true);
					return;
				}
			}
		});
	}
});
