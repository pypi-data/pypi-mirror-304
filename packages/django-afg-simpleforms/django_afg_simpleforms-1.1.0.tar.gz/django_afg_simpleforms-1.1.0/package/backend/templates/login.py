<!DOCTYPE html>#}
{#<html lang="en">#}
{#<head>#}
{#    <meta charset="UTF-8">#}
{#</head>#}
{#<body>#}
{#    <form method="POST">#}
{#        {% csrf_token %}#}
{#        {{ form }}#}
{#        <button type="submit">Войти</button>#}
{#    </form>#}
{#    <div>#}
{#        Ещё не зарегистрированы? <a href="{% url 'registration' %}">Зарегистрироваться</a>#}
{#    </div>#}
{#</body>#}
{#</html>