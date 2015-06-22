var app = app || {};

app.AddPersonView = Backbone.View.extend({

	el: '#js_add_person_form',

    events: {
        'click #js-add-person': 'addPerson'
    },

    templates: {
        associated_with: _.template( $('#jst-associated-with').html() )
    },

    initialize: function(){
    	this.renderAssociatedWith();
    	this.listenTo( app.expense_books, 'add', this.renderAssociatedWith );
        this.listenTo( app.expense_books, 'reset', this.renderAssociatedWith );
        this.model = new app.Person({}, {
            collection: app.people
        });
    },

    renderAssociatedWith: function(){
        this.$('#js-associated-with').html(
            this.templates.associated_with(
                {'expense_books': app.expense_books.toJSON()}));
    },

    addPerson: function( e ){
        $('#js-add-person').button('loading');
        e.preventDefault();
        var name = $('#js-name').val();
        var email = $('#js-email').val();
        var associated_with = $('#js-associated-with').val();
        var expense_book = app.expense_books.get(associated_with);
        var created_by = app.people.toJSON()[0].resource_uri
        var formData = {'username': name, 'email': email, 'created_by':created_by }
        var self = this;
        this.model.save(formData, {
            success: function(model, response, options){
                app.people.add(model);
                self.$el.modal('hide');
                app.people.fetch({reset: true, async: false});
                var expense_book = app.expense_books.get(associated_with);
                expense_book.get('people').push(response.resource_uri);
                expense_book.save();
                app.myrouter.navigate('/all_people', true);        
            },
            error: function(model, response, options){
                debugger;
                if(options.xhr.status == 201){
                    debugger;
                    app.people.add(model);
                    self.$el.modal('hide');
                    app.people.fetch({reset: true, async: false});
                    app.myrouter.navigate('/all_people', true);        
                    return;
                }
                if ( response == "username already in use" ) {
                    $('#js-name-err').show();
                } else if ( response == "email already in use" ) {
                    $('#js-email-err').show();
                }
            }
        });
        $('#js-add-person').button('reset');
    }

});