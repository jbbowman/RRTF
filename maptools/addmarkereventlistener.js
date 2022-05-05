<!-- monkey patched Marker template -->
{% macro script(this, kwargs) %}
var {{ this.get_name() }} = L.marker(
{{ this.location|tojson }},
{{ this.options|tojson }}
).addTo({{ this._parent.get_name() }}).on('click', onClick);
{% endmacro %}