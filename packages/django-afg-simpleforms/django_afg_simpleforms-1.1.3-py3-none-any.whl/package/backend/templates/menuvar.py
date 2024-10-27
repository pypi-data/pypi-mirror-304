{% load static %}#}
{##}
{#<style>#}
{#    h3{#}
{#    margin: 0 0 0 2vw;#}
{#    padding: 0;#}
{#}#}
{##}
{#ul{#}
{#    list-style: none;#}
{#    display: flex;#}
{#    margin: 0;#}
{#    padding: 1vh 2vw 1vh 2vw;#}
{#    align-items: center;#}
{#    z-index:10;#}
{#}#}
{##}
{#li{#}
{#    margin-left: 5vw;#}
{#}#}
{##}
{#.login{#}
{#    margin-left:auto;#}
{#    margin-right: 0;#}
{#    display: flex;#}
{#}#}
{##}
{#.login button {#}
{#    margin-left: 2vw;#}
{#}#}
{#button {#}
{#    background-color: transparent;#}
{#    border: 2px solid white;#}
{#    color: white;#}
{#    padding: 1vh;#}
{#    transition: background-color 0.3s, color 0.3s;#}
{#    cursor: pointer;#}
{#}#}
{##}
{#button:hover {#}
{#    background-color: rgba(255, 255, 255, 0.1);#}
{#}#}
{##}
{#a{#}
{#    text-decoration: none;#}
{#    color: azure;#}
{#}#}
{##}
{#menu{#}
{#    margin: 0;#}
{#    padding: 0;#}
{#    background-color: black;#}
{#}#}
{##}
{#body{#}
{#    margin: 0;#}
{#    padding: 0;#}
{#}#}
{##}
{#.logo{#}
{#    max-height:9vh;#}
{#    max-width: auto;#}
{#}#}
{##}
{#</style>#}
{#<menu>#}
{#<ul>#}
{#    <a href="{% url 'index' %}"><img class="logo" src="{% static 'images/logo.png'%}" alt="logo"></a>#}
{#    <a href="{% url 'index' %}"><h3>ИНТЕР</h3></a>#}
{#    <li><a href="{% url 'index' %}">ГЛАВНАЯ</a></li>#}
{#    <li><a href="{% url 'catalog' %}">КАТАЛОГ</a></li>#}
{#    <li><a href="{% url 'contacts' %}">КОНТАКТЫ</a></li>#}
{#    <div class="login">#}
{#    <a href="{% url 'login' %}"><button>АВТОРИЗАЦИЯ</button></a>#}
{#    <a href="{% url 'register' %}"><button>РЕГИСТРАЦИЯ</button></a>#}
{#    </div>#}
{#</ul>#}
{#</menu>