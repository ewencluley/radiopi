$(document).ready(function() {
    function saving() {
        $("#savingIcon").attr("class", "fas fa-circle-notch fa-spin")
    }
    function saving_complete() {
        $("#savingIcon").attr("class", "fas fa-check-circle")
    }
    function ajaxCallRequest(f_method, f_url, f_data, on_success) {
        $("#dataSent").val(unescape(f_data));
        let f_contentType = 'application/json; charset=UTF-8';
        $.ajax({
            url: f_url,
            type: f_method,
            contentType: f_contentType,
            dataType: 'json',
            data: f_data,
            success: on_success
        });
    }

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