{% extends "mail_templated/base.tpl" %}

{% block subject %}
<h2>  لینک فعالسازی و وریفای  اکانت شما</h2>
{% endblock %}

{% block html %}
<p><a href="{% url 'accounts:activation' token=token %}"><h2>لینک فعالسازی </h2></a></p>
{% endblock %}