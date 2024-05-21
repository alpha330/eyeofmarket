{% extends "mail_templated/base.tpl" %}

{% block subject %}
<h2> ایمیل تایید دریافت تیکت شما </h2>
{% endblock %}

{% block html %}
<h3>{{email}}<h3>
<p><h2>{{first_name}}</h2></p>
<p><h2>{{last_name}}</h2></p>
<p><h2>درخواست شما ثبت شده است </h2></p>
{% endblock %}