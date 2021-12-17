<ul class="nav flex-column">
    <li class="nav-item">
        {% for menu in menuToShow %}
            {% if menu.selected %}
                <a class="nav-link" href="{{linkPrefix}}{{ menu.link }}" data-id="{{ menu.id }}">
                    {{ menu.title }}
                </a>
            {% else %}
                <a class="nav-link not-selected" href="{{linkPrefix}}{{ menu.link }}" data-id="{{ menu.id }}">
                    {{ menu.title }}
                </a>
            {% endif %}
            {% if menu.children %}
                {{ menu.children }}
            {% endif %}
        {% endfor %}
    </li>
</ul>
