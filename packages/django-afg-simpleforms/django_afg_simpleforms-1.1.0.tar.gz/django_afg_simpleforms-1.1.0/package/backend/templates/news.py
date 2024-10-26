<!DOCTYPE html>#}
{#<html lang="en">#}
{#<head>#}
{#    <meta charset="UTF-8">#}
{#    <meta name="viewport" content="width=device-width, initial-scale=1.0">#}
{#    <title>News</title>#}
{#    {% load static %}#}
{#    <link rel="stylesheet" type="text/css" href="{% static 'css/button.css' %}">#}
{#    <link rel="stylesheet" type="text/css" href="{% static 'css/h1.css' %}">#}
{#    <style>#}
{#        body{#}
{#            background-image: url("{% static 'images/фон.svg' %}");#}
{#            background-size: 100%;#}
{#            background-repeat: no-repeat;#}
{#        }#}
{#        #}
{#        .news {#}
{#            background-color: #fefefecb;#}
{#            padding: 15px;#}
{#        }#}
{#    </style>#}
{#</head>#}
{#<body>#}
{#{% include "base/menu.html" %}#}
{#<div style="margin-left: 2.5vw; margin-right: 2.5vw;">#}
{#<h2>News</h2>#}
{##}
{#<form method="GET" action=".">#}
{#    <label for="sort">Sort by:</label>#}
{#    <select id="sort" name="sort">#}
{#        <option value="-date" {% if request.GET.sort == '-date' %}selected{% endif %}>Newest First</option>#}
{#        <option value="date" {% if request.GET.sort == 'date' %}selected{% endif %}>Oldest First</option>#}
{#    </select>#}
{#    <button type="submit">Sort</button>#}
{#</form>#}
{##}
{#{% if news %}#}
{#    {% for news_item in news %}#}
{#        <div class="news">#}
{#            <h3>{{ news_item.title }}</h3>#}
{#            <p>Date: {{ news_item.date }}</p>#}
{#            <p>{{ news_item.description|truncatewords_html:30 }} <a href="/news/{{ news_item.news_id}}/">Read more</a></p>#}
{#        </div>#}
{#        <hr>#}
{#    {% empty %}#}
{#        <p>No news available.</p>#}
{#    {% endfor %}#}
{##}
{#    {% if news.has_other_pages %}#}
{#        <div class="pagination">#}
{##}
{#               {% for num in news.paginator.page_range %}#}
{#                {% if news.number == num %}#}
{#                    <span class="current"><button class="buttone">{{ num }}</button></span>#}
{#                {% else %}#}
{#            <a href="?page={{ num }}{% if request.GET.sort %}&sort={{ request.GET.sort }}{% endif %}"><button>{{ num }}</button></a>#}
{#                {% endif %}#}
{#            {% endfor %}#}
{##}
{#            {% if news.has_previous %}#}
{#                <a href="?page=1{% if request.GET.sort %}&sort={{ request.GET.sort }}{% endif %}"><button>First</button></a>#}
{#                <a href="?page={{ news.previous_page_number }}{% if request.GET.sort %}&sort={{ request.GET.sort }}{% endif %}"><button>Previous</button></a>#}
{#            {% endif %}#}
{##}
{#            {% if news.has_next %}#}
{#                <a href="?page={{ news.next_page_number }}{% if request.GET.sort %}&sort={{ request.GET.sort }}{% endif %}"><button>Next</button></a>#}
{#                <a href="?page={{ news.paginator.num_pages }}{% if request.GET.sort %}&sort={{ request.GET.sort }}{% endif %}"><button>Last</button></a>#}
{#            {% endif %}#}
{##}
{#            <span class="current">#}
{#                Page {{ news.number }} of {{ news.paginator.num_pages }}.#}
{#            </span>#}
{#        </div>#}
{#    {% endif %}#}
{#{% else %}#}
{#    <p>No news available.</p>#}
{#{% endif %}#}
{#</div>#}
{##}
{#</body>#}
{#</html>