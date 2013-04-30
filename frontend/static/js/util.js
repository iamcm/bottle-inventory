Util = {}

Util.Html = {
    /**
     * obj.content
     * obj.id
     * obj.classname
     * obj.style
     */
    div:function(obj){
        
        var id = (obj.id) ? ' id="'+ obj.id +'"' : '' ;
        var classname = (obj.classname) ? ' class="'+ obj.classname +'"' : '' ;
        var style = (obj.style) ? ' style="'+ obj.style +'"' : '' ;
        
        return '<div'+ id + classname + style +'>'+ obj.content +'</div>';
        
    },
    
    /**
     * obj.content
     * obj.id
     * obj.classname
     * obj.style
     * obj.title
     */
    span:function(obj){
        
        var id = (obj.id) ? ' id="'+ obj.id +'"' : '' ;
        var classname = (obj.classname) ? ' class="'+ obj.classname +'"' : '' ;
        var style = (obj.style) ? ' style="'+ obj.style +'"' : '' ;
        var title = (obj.title) ? ' title="'+ obj.title +'"' : '' ;
        
        return '<span'+ id + classname + style + title +'>'+ obj.content +'</span>';
    }    
}

Util.String = {
    trim:function(string, maxlength, addTitle){       
        if(string.length > length){
            var output = string.slice(0, maxlength) + '...';
            
            if(addTitle){
                output = Util.Html.span({
                    'content':output,
                    'title':string
                })
            }
        } else {
            var output = string;
        }   
        
        return output;
    }
}

Util.Templating = {
    renderTemplate:function(templateid, context, targetid, fadeInEl){
        var source = $('#'+ templateid).html();
        source = source.replace(/\[\[/g, '{{');
        source = source.replace(/\]\]/g, '}}');
        var template = Handlebars.compile(source);
        $('#'+ targetid).html(template(context));
        $(fadeInEl).fadeIn(50);
    }
}