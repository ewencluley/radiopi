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
    loading()
    ajaxCallRequest("GET", "/api/v1/alarm", null, function (data) {
                $("#alarmTime").val(data.time);
                $("#alarmDuration").val(data.durationMinutes);
                for (let i = 0; i < 7; i++) {
                    if (data.daysOfWeek.includes(i)) {
                        $("#daysOfWeek :input[value=" + i + "]").attr('checked', true)
                        $("#daysOfWeek :input[value=" + i + "]").parent().addClass('active')
                    }
                }
                $("#alarmEnabled").prop('checked', data.enabled).change()
                loading_complete()
            })
});