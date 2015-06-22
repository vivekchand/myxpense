var app = app || {};

app.People = Backbone.Collection.extend({
    model: app.Person,
    url: '/api/v1/person/'
});