<ul class="folder-breadcrump">
    {% for folderTitle, folderLink in folderList %}
        <li>
            {% if folderLink %}
                <a href="{{ linkPrefix }}{{ folderLink }}">{{ folderTitle }}</a>
            {% else %}
                {{ folderTitle }}
            {% endif %}
        </li>
    {% endfor %}
</ul>