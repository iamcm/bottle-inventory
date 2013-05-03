var Collection = {
    collections:null,

    getAll:function(callback){
        var self = this;

        $.getJSON('/collections', function(json){
            self.collections = json;

            Util.Templating.renderTemplate('collection_template', {'collections':json}, 'collections');

            if(callback) callback();
        })
    },

    getDropdown:function(){
        if(!this.collections){
            this.getAll(this.getDropdown);
        } else {

            var html = Util.Html.select({
                name:'collectionId',
                content:this.collections,
                valueKey:'_id',
                nameKey:'name',
            });

            return html;
        }

    },

    save:function(params, callback){
        $.post('/collection', params, function(){
            if(callback) callback();
        })
    },

    attachEvents:function(){
        var self = this;

        $('#formAddCollection').on('submit', function(ev){
            ev.preventDefault();

            var params = $(this).serialize();

            self.save(params, function(){
                window.location = '/frontend/index.html';
            });

        })
    }
}

var Item = {
    getAll:function(collection_id){
        if(collection_id) data = {collectionId:collection_id}
        $.getJSON('/items', data, function(json){
            Util.Templating.renderTemplate('item_template', {'items':json}, 'items');
        })
    },

    save:function(params, callback){
        $.post('/item', params, function(){
            if(callback) callback();
        })
    },

    attachEvents:function(){
        var self = this;

        $('#aAddItem').on('click', function(){
            $('#dropCollectionsContainer').html(Collection.getDropdown());

            $('#formAddItem').toggle();
        });    

        $('#formAddItem').on('submit', function(ev){
            ev.preventDefault();

            var params = Util.querystringToObject( $(this).serialize() );
            params.collectionIds = [params.collectionId];

            self.save(params, function(){
                window.location = '/frontend/index.html';
            });

        })
    }
}

Path.map("#/home").to(function(){
    Collection.getAll();
    Collection.attachEvents();
    Item.attachEvents();
});

Path.map("#/collection/:id").to(function(){
    Item.getAll(this.params["id"])
});

Path.root("#/home");

Path.listen();