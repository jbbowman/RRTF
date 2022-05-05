{% macro script(this, kwargs) %}
function getInnerText( sel ) {
    var txt = '';
    $( sel ).contents().each(function() {
        var children = $(this).children();
        txt += ' ' + this.nodeType === 3 ? this.nodeValue : children.length ? getInnerText( this ) :
        $(this).text();
    });
    return txt;
};
function onClick(e) {
   var popup = e.target.getPopup();
   var content = popup.getContent();
   text = getInnerText(content);
   console.log(text);
};
{% endmacro %}
