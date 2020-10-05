$(document).ready(function() {

    $("#alarmForm").on('submit', event => event.preventDefault());
    $("#alarmForm").on('change',function(event) {
        if (isLoading()) {
            return;
        }
        saving();
        let form = $('#alarmForm');
        let method = form.attr('method');
        let url = form.attr('action');

        let daysOfWeek = $("#daysOfWeek :input:checked").toArray().map(function(value){
            return parseInt($(value).val());
        });
        let alarm = {
            time: $("#alarmTime").val(),
            daysOfWeek: daysOfWeek,
            enabled: $("#alarmEnabled").prop('checked'),
            durationMinutes: $("#alarmDuration").val()
        }
        let data = JSON.stringify(alarm);
        ajaxCallRequest(method, url, data, function (data) {
                let jsonResult = JSON.stringify(data);
                $("#results").val(unescape(jsonResult));
                saving_complete();
            });
    })
    $("#stopAlarm").on('click',function(event) {
        if (isLoading()) {
            return;
        }
        saving();
        let url = "/api/v1/alarm/stop"
        ajaxCallRequest('POST', url, null, saving_complete);
    })
});