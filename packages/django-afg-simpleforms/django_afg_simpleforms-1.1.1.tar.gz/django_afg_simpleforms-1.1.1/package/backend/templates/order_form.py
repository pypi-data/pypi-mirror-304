<!DOCTYPE html>#}
{#<html>#}
{#<head>#}
{#    <title>Order application</title>#}
{#    {% load static %}#}
{#</head>#}
{#<style>#}
{#    body {#}
{#        background-image: url("{% static 'images/фон.svg' %}");#}
{#        background-repeat: no-repeat;#}
{#        background-size: 100%;#}
{#    }#}
{#    #}
{##}
{#    form {#}
{#        background-color: rgba(255, 255, 255, 0.1);#}
{#        padding: 20px;#}
{#        width: 400px;#}
{#        background-color: #C3D3D3;#}
{#        margin-left: auto;#}
{#        margin-right: auto;#}
{#        margin-top: 5vh;#}
{#    }#}
{##}
{#    label {#}
{#        margin-top: 10px;#}
{#        display: block;#}
{#    }#}
{##}
{#    input[type="text"],#}
{#    input[type="email"],#}
{#    textarea,#}
{#    select {#}
{#        width: 100%;#}
{#        padding: 10px;#}
{#        border: 1px solid #ccc;#}
{#        border-radius: 5px;#}
{#        box-sizing: border-box;#}
{#    }#}
{##}
{#</style>#}
{#<body>#}
{#{% include "base/menu.html" %}#}
{##}
{#<form method="post">#}
{#    {% csrf_token %}#}
{#    <h2>Оставить заявку на заказ</h2>#}
{#    <label for="name">Имя:</label><br>#}
{#    <input type="text" id="name" name="name" required><br><br>#}
{##}
{#    <label for="email">Email:</label><br>#}
{#    <input type="email" id="email" name="email" required><br><br>#}
{##}
{#    <label for="category">Категория:</label><br>#}
{#    <select id="category" name="category" required>#}
{#        {% for category in categories %}#}
{#        <option value="{{ category.category_id }}">{{ category.name }}</option>#}
{#        {% endfor %}#}
{#    </select><br><br>#}
{##}
{#    <label for="description">Описание:</label><br>#}
{#    <textarea id="description" name="description" rows="15" cols="50"></textarea><br><br>#}
{##}
{#    <input type="submit" value="Отправить">#}
{#</form>#}
{#</body>#}
{#</html>