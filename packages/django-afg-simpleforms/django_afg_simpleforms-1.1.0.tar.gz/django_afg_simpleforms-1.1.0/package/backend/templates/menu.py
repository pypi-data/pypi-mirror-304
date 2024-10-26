{#<!DOCTYPE html>#}
{#<html lang="en">#}
{#<head>#}
{#    <meta charset="UTF-8">#}
{#    {% load static %}#}
{#    <link rel="stylesheet" type="text/css" href="{% static 'css/mene.css' %}">#}
{#    <link rel="stylesheet" type="text/css" href="{% static 'css/h1.css' %}">#}
{#</head>#}
{#<body>#}
{#<nav>#}
{#    <div class="burger-menu">&#9776;</div>#}
{#    <div class="close-menu">&times;</div>#}
{#    <ul>#}
{#        <li><a href="{% url 'index' %}">HOME</a></li>#}
{#        <li><a href="{% url 'illustration' %}">ILLUSTRATION</a></li>#}
{#        <li><a href="{% url 'engraving' %}">ENGRAVING</a></li>#}
{#        <li><a href="{% url 'replica' %}">REPLICA</a></li>#}
{#        <li><a href="{% url 'abstraction' %}">ABSTRACTION</a></li>#}
{#        <li><a href="{% url 'interpretation' %}">INTERPRETATION</a></li>#}
{#        <li><a href="{% url 'decorative_art' %}">DECORATIVE ART</a></li>#}
{#        <li><a href="{% url 'about' %}">ABOUT</a></li>#}
{#        <li><a href="{% url 'contacts' %}">CONTACTS</a></li>#}
{#        <li><a href="{% url 'order_form' %}">ORDER APPLICATION</a></li>#}
{#        <li><a href="{% url 'news' %}">NEWS</a></li>#}
{##}
{#        {% if user.is_authenticated %}#}
{#            <li>#}
{#                <a href="#" id="username">{{ user.username }}</a>#}
{#                <form id="logout-form" action="{% url 'logout' %}" method="post" style="display:none;">#}
{#                    {% csrf_token %}#}
{#                </form>#}
{#            </li>#}
{#        {% else %}#}
{#            <li><a href="{% url 'login' %}">LOGIN/REGISTER</a></li>#}
{#        {% endif %}#}
{#    </ul>#}
{#</nav>#}
{#<script>#}
{#document.addEventListener('DOMContentLoaded', function() {#}
{#    const burgerMenu = document.querySelector('.burger-menu');#}
{#    const closeMenu = document.querySelector('.close-menu');#}
{#    const navList = document.querySelector('nav ul');#}
{##}
{#    function closeNavMenu() {#}
{#        navList.classList.remove('open');#}
{#        closeMenu.style.display = 'none';#}
{#    }#}
{##}
{#    burgerMenu.addEventListener('click', function() {#}
{#        navList.classList.toggle('open');#}
{#        closeMenu.style.display = 'block';#}
{#    });#}
{##}
{#    closeMenu.addEventListener('click', function() {#}
{#        closeNavMenu();#}
{#    });#}
{##}
{#    document.addEventListener('click', function(event) {#}
{#        if (!navList.contains(event.target) && event.target !== burgerMenu) {#}
{#            closeNavMenu();#}
{#        }#}
{#    });#}
{##}
{#    window.addEventListener('resize', function() {#}
{#        if (window.innerWidth > 768) {#}
{#            closeNavMenu();#}
{#        }#}
{#    });#}
{##}
{#    // Добавляем обработчик для выхода из системы#}
{#    document.getElementById('username')?.addEventListener('click', function(e) {#}
{#        e.preventDefault();#}
{#        const confirmLogout = confirm("Вы уверены, что хотите выйти?");#}
{#        if (confirmLogout) {#}
{#            document.getElementById('logout-form').submit();#}
{#        }#}
{#    });#}
{#});#}
{#</script>#}
{#</body>#}
{#</html>#}
