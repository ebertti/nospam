Contador = Backbone.Model.extend({

    initialize: function(){
        this.set({
            qtd:0,
            com_link:0,
            sem_link:0
        });
        _.bindAll(this, 'mais_um');
    },

    mais_um: function(com_link){
        this.set('qtd', this.get('qtd') + 1, {silent:true});
        if(com_link){
            this.set('com_link', this.get('com_link') + 1, {silent:true});
        } else {
            this.set('sem_link', this.get('sem_link') + 1, {silent:true});
        }
        this.trigger('change');
    }
});