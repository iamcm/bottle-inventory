var EventRegistry = []

var Router = {
    showPage:function(id){
        $('.page').hide();
        $('#'+ id).show();
    }
}

var Collection = {
    collections:null,

    getAll:function(callback){
        var self = this;

        $.getJSON('/api/collections', function(json){
            self.collections = json;

            Util.Templating.renderTemplate('collection_template', {'collections':json}, 'collections');

            if(callback) callback();
        })
    },

    getDropdown:function(callback){

        if(!this.collections){
            var self = this;

            this.getAll(function(){
                self.getDropdown(callback);
            });
        } else {
            var html = Util.Html.select({
                name:'collectionId',
                content:this.collections,
                valueKey:'_id',
                nameKey:'name',
            });

            callback(html);
        }
    },

    save:function(params, callback){
        $.post('/api/collection', params, function(){
            if(callback) callback();
        })
    },

    attachEvents:function(){
        var self = this;

        var eventName = "formAddCollection";

        if(EventRegistry.indexOf(eventName) == -1){            
            EventRegistry.push(eventName);

            $('#formAddCollection').on('submit', function(ev){
                ev.preventDefault();

                var params = $(this).serialize();

                self.save(params, function(){
                    window.location = '/index.html';
                });

            })
        }
    }
}

var Item = {
    getOne:function(item_id){

        $.getJSON('/api/item/'+item_id, function(json){
            Util.Templating.renderTemplate('item_template', json, 'items');
        })
    },
    
    getAll:function(collection_id){
        if(collection_id) data = {collectionId:collection_id}
        $.getJSON('/api/items', data, function(json){
            Util.Templating.renderTemplate('item_list_template', {'items':json}, 'items');
        })
    },

    save:function(params, callback){
        $.post('/api/item', params, function(){
            if(callback) callback();
        })
    },

    attachEvents:function(){
        var self = this;

        var eventName = "formAddItem";

        if(EventRegistry.indexOf(eventName) == -1){            
            EventRegistry.push(eventName);

            $('#formAddItem').on('submit', function(ev){
                ev.preventDefault();
                
                var params = Util.querystringToObject( $(this).serialize() );
                params.collectionIds = [params.collectionId];
                
                var uploader = $('#uploader').pluploadQueue();

                if (uploader.files.length > 0) {
                    uploader.bind('StateChanged', function() {
                        if (uploader.files.length === (uploader.total.uploaded + uploader.total.failed)) {

                            self.save(params, function(){
                                window.location = '#/collection/'+ params.collectionId;
                            });

                        }
                    });

                    uploader.start();
                }else{
                    self.save(params, function(){
                        window.location = '#/collection/'+ params.collectionId;
                    });
                }
            })
        }
    }
}


$(document).ajaxError(function(event, jqxhr){
    if(jqxhr.status == 403){
        window.location = '/login.html';
    } else {
        Util.flashMessage('error', 'An error has occured');
    }
})

Path.map("#/home").to(function(){
    Collection.getAll();
    Router.showPage('pageHome');
});

Path.map("#/collection/add").to(function(){
    Collection.attachEvents();
    Router.showPage('pageAddCollection');
});

Path.map("#/item/add").to(function(){
    Item.attachEvents();

    Collection.getDropdown(function(html){
        $('#dropCollectionsContainer').html(html);
    })

    Router.showPage('pageAddItem');
});

Path.map("#/collection/:id").to(function(){
    Router.showPage('pageHome');
    Item.getAll(this.params["id"])
});

Path.map("#/item/:id").to(function(){
    Router.showPage('pageHome');
    Item.getOne(this.params["id"])
});

Path.root("#/home");

Path.listen();