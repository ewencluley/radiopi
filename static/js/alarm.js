$(document).ready(function() {

    $("#alarmForm").on('change',function(event) {
        saving();
        event.preventDefault();
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
        }
        let data = JSON.stringify(alarm);
        ajaxCallRequest(method, url, data, function (data) {
                let jsonResult = JSON.stringify(data);
                $("#results").val(unescape(jsonResult));
                saving_complete();
            });
    });

    ajaxCallRequest("GET", "/api/v1/alarm", null, function (data) {
                $("#alarmTime").val(data.time);
                for (let i = 0; i < 7; i++) {
                    $("#daysOfWeek :input[value=" + i + "]").prop('checked', data.daysOfWeek.includes(i))
                }
                $("#alarmEnabled").prop('checked', data.enabled).change()
            })
});