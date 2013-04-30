
var Collection = Backbone.Model.extend({
	url: '/collection',
	defaults: {
		_id:null,
        name: null,
        added:null
    }
});

var Item = Backbone.Model.extend({
	url: '/item',
	defaults: {
        name: '',
        collectionIds:[]
    }
});

var CollectionFormView = Backbone.View.extend({
    initialize: function(){
        $('#collection_name').val('');
    },

    events: {
        "click #submit": "saveCollection"  
    },
    saveCollection: function( event ){
        var c = new Collection();
        c.set(name, $('#collection_name').val());
        c.save();
        
        this.initialize();
        collections_view.initialize();
    }
});


var CollectionsView = Backbone.View.extend({
    initialize: function(){
        this.render();
    },
    render: function(){
    	var self = this;

    	var collections = new Collections();
    	collections.fetch({
    		success:function(collections){
    			var template = _.template( $("#collection_template").html(), {collections:collections.models} );
		        self.$el.html( template );
    		}
    	});
        
    }
});

var Router = Backbone.Router.extend({

  routes: {
    "collection/:id":        "collection"  // #search/kiwis
  },

  collection: function(id) {
    alert(id)
  }

});

var r = new Router();
Backbone.history.start();

var Collections = Backbone.Collection.extend({
  model: Collection,
  url:'/collections'
});
    
var collection_form_view = new CollectionFormView({ el: $("#collection_form") });
var collections_view = new CollectionsView({ el: $("#collections") });