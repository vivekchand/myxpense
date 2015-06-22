var app = app || {};
app.AddPersonModalView = Backbone.View.extend({
	el: '#js-add-person-modal',
	
	events: {
		'click #js-modal-add-person': 'addPerson'
	},

	initialize: function(){
		this.model = new app.Person({}, {
			collection: app.people
		});
	},

	show: function(){
		this.$el.modal('show');
	},

	addPerson: function( e ){
		$('#js-modal-add-person').button('loading');

		e.preventDefault();
		var name = $('#js-name').val();
		var email = $('#js-email').val();
		var created_by = app.people.toJSON()[0].resource_uri
		var formData = {'username': name, 'email': email, 'created_by':created_by }
		var self = this;
		app.people.create(new app.Person(formData), {
			success: function(model, response, options){
				app.people.fetch({reset: true, async: false});
				self.$el.modal('hide');
			},
			error: function(model, response, options){
				if ( response == "username already in use" ) {
					$('#js-name-err').show();
				} else if ( response == "email already in use" ) {
					$('#js-email-err').show();
				} else {
					app.people.fetch({reset: true, async: false});
					self.$el.modal('hide');
				}
			}
		});
		$('#js-modal-add-person').button('reset');
	}
});