<div class="table-responsive">
    <table class="table table-striped table-sm">
        <thead>
            <tr>
                <th>Date</th>
                <th>From</th>
                <th>To</th>
                <th>Subject</th>
                <th>Size</th>
                <th></th>
                <th></th>
            </tr>
        </thead>
        <tbody>
            {% for mail in mailList %}
                <tr data-id="{{ mailList[mail].id }}">
                    <td>{{ mailList[mail].date }}</td>
                    <td>{{ mailList[mail].from }}</td>
                    <td>{{ mailList[mail].to }}</td>
                    <td><a href="{{ linkPrefix }}{{ mailList[mail].link }}">{{ mailList[mail].subject }}</a></td>
                    <td>{{ mailList[mail].size }}</td>
                    <td>
                        {% if mailList[mail].attachments %}
                            <i class="bi bi-paperclip" title="{{ mailList[mail].attachments }} attachment(s)"></i>
                        {% endif %}
                    </td>
                    <td>
                        {% if mailList[mail].error_decoding %}
                            <i class="bi bi-exclamation-octagon btn-outline-danger" title="{{ mailList[mail].error_decoding }}"></i>
                        {% endif %}
                    </td>
                </tr>
            {% else %}
                <tr><td colspan="5">Folder is empty</td></tr>
            {% endfor %}
        </tbody>
    </table>
</div>