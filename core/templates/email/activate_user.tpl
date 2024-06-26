{% extends "mail_templated/base.tpl" %}

{% block subject %}
<h2>  لینک فعالسازی و وریفای  اکانت شما</h2>
{% endblock %}

{% block html %}
<h3>{{email}}<h3>
<p><h2>{{first_name}}</h2></p>
<p><h2>{{last_name}}</h2></p>
<p><h2>لینک فعالسازی </h2></p>
{% endblock %}