<div>
    <table class="datatable table table-striped table-bordered">
        <thead>
            <tr>
                <th>Date</th>
                <th>From</th>
                <th>To</th>
                <th>Subject</th>
                <th>Size</th>
                <th></th>
            </tr>
        </thead>
        <tbody>
            {% for mail in mailList %}
                <tr data-id="{{ mailList[mail].id }}">
                    <td class="align-center"><span class="nobr">{{ mailList[mail].date }}</span></td>
                    <td>{{ mailList[mail].from|simplifyEmailHeader }}</td>
                    <td>{{ mailList[mail].to|simplifyEmailHeader }}</td>
                    <td>
                        {% if mailList[mail].error_decoding %}
                            <i class="bi bi-exclamation-octagon btn-outline-danger" title="{{ mailList[mail].error_decoding }}" />
                        {% endif %}
                        <a href="{{ linkPrefix }}{{ mailList[mail].link }}">{{ mailList[mail].subject|e }}</a>
                    </td>
                    <td class="align-right" data-order="{{ mailList[mail].size }}"><span class="nobr">{{ mailList[mail].size|humansize }}<span></td>
                    <td class="align-center">
                        {% if mailList[mail].attachments %}
                            <i class="bi bi-paperclip" title="{{ mailList[mail].attachments }} attachment(s)" />
                        {% endif %}
                    </td>
                </tr>
            {% else %}
                <tr><td colspan="7">Folder is empty</td></tr>
            {% endfor %}
        </tbody>
    </table>
</div>