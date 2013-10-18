Contadores = Backbone.Collection.extend({

    comparator: 'id',

    model: function(){
        return Contador;
    },

    initialize: function(){
        this.qtd = 0;
        this.com_link = 0;
        this.sem_link = 0;
        _.bindAll(this, 'mais_um');
    },

    mais_um: function(idioma, com_link){
        var contador = this.get(idioma);
        if(!contador){
            contador = new Contador({
                id: idioma
            });
            this.add(contador);
        }
        contador.mais_um(com_link);
        this.qtd++;
        if(com_link){
            this.com_link++;
        } else {
            this.sem_link++;
        }
    }

});