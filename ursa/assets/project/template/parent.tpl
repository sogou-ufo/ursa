<!doctype html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>{% block page_title %}{% endblock %}</title>
        <link rel="stylesheet" href="/static/css/main.css" type="text/css" />
    </head>
    <body {% block body_class %}{% endblock %}>
        {% block content %}{% endblock %}
    </body>
    <script type="text/javascript" src="http://p0.123.sogou.com/u/js/ufo2.js"></script>
    <script type="text/javascript">
        
require.config({
    baseUrl:"/static/js",
    urlArgs:"t=@tm:/static/js/main.js@"
});

require(['main'] , function(main){
    main.common && main.common();
    main['{{_token}}'] && main['{{_token}}']();
});

    </script>
</html>
