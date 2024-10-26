<!DOCTYPE html>#}
{#<html lang="en">#}
{#<head>#}
{#    <meta charset="UTF-8">#}
{#    <meta name="viewport" content="width=device-width, initial-scale=1.0">#}
{#    <title>News Details</title>#}
{#</head>#}
{#<body>#}
{#{% include "base/menu.html" %}#}
{#<div>#}
{#    <h2>{{ news_item.title }}</h2>#}
{#    <p>Date: {{ news_item.date }}</p>#}
{#    <p>{{ news_item.description }}</p>#}
{#    {% if news_item.image %}#}
{#    <img src="{{ news_item.image.url }}" alt="{{ news_item.title }}">#}
{#    {% endif %}#}
{#    <p><a href="/news/">Back to News</a></p>#}
{#</div>#}
{##}
{#</body>#}
{#</html>