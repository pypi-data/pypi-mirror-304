{#<!DOCTYPE html>#}
{#<html lang="en">#}
{#<head>#}
{#    <meta charset="UTF-8">#}
{#    <meta name="viewport" content="width=device-width, initial-scale=1.0">#}
{#    <title>{{ news_item.title }}</title>#}
{#    {% load static %}#}
{#    <link rel="stylesheet" type="text/css" href="{% static 'css/h1.css' %}">#}
{#    <style>#}
{#        body {#}
{#            background-image: url("{% static 'images/фон.svg' %}");#}
{#            background-repeat: no-repeat;#}
{#            background-size: 100%;#}
{#        }#}
{#    </style>#}
{#</head>#}
{#<body>#}
{##}
{#<h1>{{ news_item.title }}</h1>#}
{##}
{#<div>#}
{#    <p>{{ news_item.description }}</p>#}
{#    <p>Date: {{ news_item.date }}</p>#}
{#    {% if news_item.image %}#}
{#    <img src="{{ news_item.image.url }}" alt="{{ news_item.title }}">#}
{#    {% endif %}#}
{#</div>#}
{##}
{#</body>#}
{#</html>#}
