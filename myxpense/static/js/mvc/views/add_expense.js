var app = app || {};

app.AddExpenseView = Backbone.View.extend({
    el: '#js_add_expense_form',

    events: {
        'click #add': 'addExpense',
        'change #js-associated-with': 'changeAssociatedWith',
        'change #js-paid-by': 'renderSharedWith',

        'click #js-also-paid-by': 'renderAlsoPaidBy'
    },

    templates: {
        associated_with: _.template( $('#jst-associated-with').html() ),
        shared_with: _.template( $('#jst-shared-with').html() ),
        also_paid_by: _.template( $('#jst-also-paid-by').html() )
    },    

    initialize: function(){
        this.renderAssociatedWith();
        this.renderPaidBy();
        this.listenTo( app.expense_books, 'add', this.renderAssociatedWith );
        this.listenTo( app.expense_books, 'reset', this.renderAssociatedWith );
    },

    hideAmountErr: function() {
        var amt_err = $('[id="js-paid-by-amount"]').last().find('[id="js-amount-err"]').hide();
        amt_err.parent().removeClass('has-error');
    },

    showAmountErr: function() {
        var amt_err = $('[id="js-paid-by-amount"]').last().find('[id="js-amount-err"]').show();
        amt_err.parent().addClass('has-error');
    },

    renderAssociatedWith: function(){
        if( app.expense_books.length <= 0 ) {
            this.$('#js-expense-warning').show();
            this.$('#js-expense-name').prop('disabled', true);
            this.$('#js-associated-with').prop('disabled', true);
            this.$('#js-expense-type').prop('disabled', true);
            this.$('#js-paid-by').prop('disabled', true);
            this.$('#js-amount').prop('disabled', true);
            this.$('#js-also-paid-by').prop('disabled', true);
            this.$('#add').prop('disabled', true);
        }
        this.$('#js-associated-with').html(
            this.templates.associated_with(
                {'expense_books': app.expense_books.toJSON()}));
    },

    changeAssociatedWith: function(){
        this.renderPaidBy();
    },

    renderPaidBy: function(){
        var expbook_uri = $('#js-associated-with option:selected')[0].value;
        var expbook = app.expense_books.get({'id': expbook_uri});

        var people_uri = expbook.toJSON().people;
        var paid_by = _.map(people_uri, function(person_uri){ 
                    return app.people.get({'id': person_uri}).toJSON()
        });
        this.$('#js-paid-by-list').html(
            this.templates.also_paid_by({'paid_by': paid_by}));
        this.renderAlsoPaidByLink(paid_by.length);
        this.hideAmountErr();
    },

    renderAlsoPaidByLink: function(paid_by_len){
        if ( paid_by_len <= 1 ) {
            $('#js-also-paid-by').hide();
            $('#js-shared-with-section').hide();
        }
        else {
            $('#js-also-paid-by').show();
            $('#js-shared-with-section').show();
            this.renderSharedWith();
        }
    },

    renderSharedWith: function(){
        var expbook_uri = $('#js-associated-with option:selected')[0].value;
        var expbook = app.expense_books.get({'id': expbook_uri});
        var all_paid_by_uri = expbook.toJSON().people;
        var the_paid_by_uri = _.map(this.$('[id="js-paid-by"] option:selected'), function(
            person){ return person.value 
        });
        var shared_with_uri = _.difference(all_paid_by_uri, the_paid_by_uri);
        var shared_with = _.map(shared_with_uri, function(person_uri){
            return app.people.get({'id': person_uri}).toJSON();
        });
        this.$('#js-shared-with-list').html(
            this.templates.shared_with({'shared_with': shared_with}));
    },

    addExpense: function(e) {
        e.preventDefault();
        $('#add').button('loading');
        var associated_with = $('#js-associated-with').val();
        var expense_type = $('#js-expense-type').val();
        var expense_name = $('#js-expense-name').val();
        var _paid_by_amount_list = _.zip($('[id="js-paid-by"]'), $('[id="js-amount"]'));
        var paid_by_amount_list = _.map(_paid_by_amount_list,
                                function(item){return {'person':item[0].value,
                                                       'amount':item[1].value};});

        var shared_with_amount_list = _.map($('input:checked'), function(item){
            return item.value;
        });
        
        var formData = {
            'associated_with': associated_with,
            'expense_type': expense_type,
            'expense_name': expense_name,
            'paid_by': paid_by_amount_list,
            'shared_with': shared_with_amount_list,
        };

        app.expenses.create(new app.Expense(formData));
        app.expenses.fetch({reset: true, async: false});
        $('#add').button('reset');
        app.myrouter.navigate('/all_expenses', true);
    },

    renderAlsoPaidBy: function(e) {
        e.preventDefault();
        var last_amount = $('[id="js-paid-by-amount"]').last().find('[id="js-amount"]').val();
        if( last_amount ) {
            this.hideAmountErr();
            var last_selected_ele_val = $('[id="js-paid-by-amount"]').last().find('[id="js-paid-by"]').children('option:selected').val();
            var cloned_item = $('[id="js-paid-by-amount"]').last().clone();
            cloned_item.find('[value="'+last_selected_ele_val+'"]').remove();
            cloned_item.find('[id="js-amount"]').val('');
            this.renderAlsoPaidByLink($('[id="js-paid-by"]').last().children().length-1);
            $('#js-paid-by-list').append(cloned_item);
            this.renderSharedWith();
        }
        else {
            this.showAmountErr();
        }
    }
});
