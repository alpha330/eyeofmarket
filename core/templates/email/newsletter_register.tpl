{% extends "mail_templated/base.tpl" %}

{% block subject %}
<h2>عضویت شما با ایمیل {{}} در خبر نامه سایت</h2>
{% endblock %}

{% block html %}
<h3>{{email}}<h3>
<p><h2>حضور شما در خبرنامه سایت باعث افتخار است</h2></p>
<p><h2>آخرین اخبار و محصولات خدمت شما ارسال می شود است</h2></p>
{% endblock %}