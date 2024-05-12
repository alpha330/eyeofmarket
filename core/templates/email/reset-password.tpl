{% extends "mail_templated/base.tpl" %}

{% block subject %}
<h2>لینک تغییر رمز عبور کاربر </h2>
{% endblock %}

{% block html %}
<h3>{{user_obj.email}}<h3>
<p> <a href="{% url "accounts:reset-password" token={{token}} %}" >لینک تغییر رمز عبور</h2></a></p>
{% endblock %}