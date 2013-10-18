ContadorView = Backbone.View.extend({

    template: _.template($('#template-contador').html()),
    className: 'col-lg-2',

    initialize: function(){
        this.model.on('change', this.render, this);
    },

    render: function(){
        this.$el.html(this.template({model: this.model.attributes}))
    }

});

ContadoresView = Backbone.View.extend({
    el: '#contadores',

    initialize: function(){
        this.collection = new Contadores();
        this.collection.on('change', this.render, this);
        _.bindAll(this, 'mais_um');
    },

    render: function () {
        this.$el.empty();
        if(this.collection.length > 0) {
            this.collection.each(this.addItem, this);
        }
        return this;
    },

    addItem: function (model) {
        var contador_view = new ContadorView({
            model: model
        });
        contador_view.render();
        this.$el.append(contador_view.$el);
    },

    mais_um: function(idioma, com_link){
        this.collection.mais_um(idioma, com_link);
    }


});