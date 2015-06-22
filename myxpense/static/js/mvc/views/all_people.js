var app = app || {};


app.PersonRowView = Backbone.View.extend({
    tagName: 'tr',
    template: _.template( $('#jst-person-row').html() ),

    render: function(){
        this.$el.html( this.template( this.model.toJSON() ) );
        return this;
    }

});


app.AllPeopleView = Backbone.View.extend({
    el: '#js-person-row',

    initialize: function() {
        this.render();
        this.listenTo( app.people, 'reset', this.render );
    },

    render: function() {
        app.people.each(function(item) {
            this.renderPerson(item);
        }, this);
    },

    renderPerson: function( item ) {
        var personRowView = new app.PersonRowView({
            model: item
        });
        this.$el.append( personRowView.render().el );
    }


});
