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
{#        .buttone {#}
{#            background: black;#}
{#            color: white;#}
{#            border-radius: 4px;#}
{#            box-shadow: none;#}
{#            outline: none;#}
{#            border-color: black;#}
{#            border-style: solid;#}
{#        }#}
{##}
{#        button:hover {#}
{#            background: #7c98b5;#}
{#            border-radius: 4px;#}
{#            box-shadow: none;#}
{#            border-style: solid;#}
{#            border-color: #7c98b5;#}
{#        }#}
{##}
{#        body {#}
{#            background-image: url("{% static 'images/фон.svg' %}");#}
{#            background-size: 100%;#}
{#            background-repeat: no-repeat;#}
{#            display: flex;#}
{#            flex-direction: column; /* Выравнивание по вертикали */#}
{#            min-height: 100vh; /* Обеспечиваем минимальную высоту на весь экран */#}
{#            margin: 0; /* Убираем отступы */#}
{#        }#}
{##}
{#        .menu {#}
{#            position: fixed; /* Фиксируем меню */#}
{#            top: 0;#}
{#            left: 0;#}
{#            width: 100%; /* Полная ширина */#}
{#            z-index: 1000; /* Убедимся, что оно выше другого контента */#}
{#        }#}
{##}
{#        .content {#}
{#            display: flex; /* Используем flexbox для расположения новостей */#}
{#            flex: 1; /* Позволяем занимать оставшееся пространство */#}
{#            padding-top: 60px; /* Для отступа под фиксированным меню */#}
{#        }#}
{##}
{#        .news-container {#}
{#            width: 50vw;#}
{#            padding: 15px;#}
{#            overflow-y: auto;#}
{#            position: relative; /* Добавляем позиционирование */#}
{#        }#}
{##}
{#        .news-detail {#}
{#            width: 50vw;#}
{#            padding: 15px;#}
{#            display: none; /* Скрыто по умолчанию */#}
{#            border-left: 1px solid #ccc;#}
{#        }#}
{##}
{#        .news {#}
{#            background-color: #fefefecb;#}
{#            margin-bottom: 10px;#}
{#            padding: 10px;#}
{#        }#}
{##}
{#        .current {#}
{#            font-weight: bold;#}
{#        }#}
{#    </style>#}
{# <script>#}
{#        function showDetails(content) {#}
{#            document.getElementById('newsDetail').innerHTML = content;#}
{#            document.getElementById('newsDetail').style.display = 'block';#}
{#        }#}
{#    </script>#}
{#</head>#}
{#<body>#}
{#<div class="content">#}
{#<div class="menu">#}
{#{% include "base/menu.html" %}#}
{#</div>#}
{##}
{#<div class="news-container">#}
{#    <h2>News</h2>#}
{##}
{#    <form method="GET" action=".">#}
{#        <label for="sort">Sort by:</label>#}
{#        <select id="sort" name="sort">#}
{#            <option value="-date" {% if request.GET.sort == '-date' %}selected{% endif %}>Newest First</option>#}
{#            <option value="date" {% if request.GET.sort == 'date' %}selected{% endif %}>Oldest First</option>#}
{#        </select>#}
{#        <button type="submit">Sort</button>#}
{#    </form>#}
{##}
{#    {% if news %}#}
{#        {% for news_item in news %}#}
{#            <div class="news">#}
{#                <h3>{{ news_item.title }}</h3>#}
{#                <p>Date: {{ news_item.date }}</p>#}
{#                <p>{{ news_item.description|truncatewords_html:30 }}#}
{#                    <a href="#" onclick="showDetails('<strong>{{ news_item.title }}</strong><br>Date: {{ news_item.date }}<br>{{ news_item.description }}'); return false;">Read more</a>#}
{#                </p>#}
{#            </div>#}
{#        {% empty %}#}
{#            <p>No news available.</p>#}
{#        {% endfor %}#}
{##}
{#        {% if news.has_other_pages %}#}
{#            <div class="pagination">#}
{#                {% for num in news.paginator.page_range %}#}
{#                    {% if news.number == num %}#}
{#                        <span class="current"><button class="buttone">{{ num }}</button></span>#}
{#                    {% else %}#}
{#                        <a href="?page={{ num }}{% if request.GET.sort %}&sort={{ request.GET.sort }}{% endif %}"><button>{{ num }}</button></a>#}
{#                    {% endif %}#}
{#                {% endfor %}#}
{##}
{#                {% if news.has_previous %}#}
{#                    <a href="?page=1{% if request.GET.sort %}&sort={{ request.GET.sort }}{% endif %}"><button>First</button></a>#}
{#                    <a href="?page={{ news.previous_page_number }}{% if request.GET.sort %}&sort={{ request.GET.sort }}{% endif %}"><button>Previous</button></a>#}
{#                {% endif %}#}
{##}
{#                {% if news.has_next %}#}
{#                    <a href="?page={{ news.next_page_number }}{% if request.GET.sort %}&sort={{ request.GET.sort }}{% endif %}"><button>Next</button></a>#}
{#                    <a href="?page={{ news.paginator.num_pages }}{% if request.GET.sort %}&sort={{ request.GET.sort }}{% endif %}"><button>Last</button></a>#}
{#                {% endif %}#}
{##}
{#                <span class="current">#}
{#                    Page {{ news.number }} of {{ news.paginator.num_pages }}.#}
{#                </span>#}
{#            </div>#}
{#        {% endif %}#}
{#    {% else %}#}
{#        <p>No news available.</p>#}
{#    {% endif %}#}
{#</div>#}
{##}
{#<div class="news-detail" id="newsDetail">#}
{#    <!-- News details will be displayed here -->#}
{#</div>#}
{#</div>#}
{#</body>#}
{#</html>