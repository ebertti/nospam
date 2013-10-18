
App = Backbone.View.extend({
    el: '#geral',

    initialize: function(){
        _.bindAll(this, 'on_cotagem');
        this.contadores_view = new ContadoresView();
        var socket = io.connect('http://localhost');
        socket.on('news', this.on_cotagem);
    },

    render: function(){
        this.$el.html(this.contadores_view.render().$el);
    },

    on_cotagem: function(data){
        this.contadores_view.mais_um(data.idioma, data.com_link);
    }

});

app = new App();