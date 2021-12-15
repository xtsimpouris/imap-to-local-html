<div class="table-responsive">
    <table class="table table-striped table-sm">
        <thead>
            <tr>
                <th>Date</th>
                <th>From</th>
                <th>To</th>
                <th>Subject</th>
                <th>Size</th>
            </tr>
        </thead>
        <tbody>
            {% for mail in mailList %}
                <tr>
                    <td>{{ mailList[mail].date }}</td>
                    <td>{{ mailList[mail].from }}</td>
                    <td>{{ mailList[mail].to }}</td>
                    <td><a href="{{linkPrefix}}{{ mailList[mail].link }}">{{ mailList[mail].subject }}</a></td>
                    <td>{{ mailList[mail].size }}</td>
                </tr>
            {% else %}
                <tr><td colspan="5">Folder is empty</td></tr>
            {% endfor %}
        </tbody>
    </table>
</div>