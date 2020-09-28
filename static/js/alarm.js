$(document).ready(function() {
    function ajaxCallRequest(f_method, f_url, f_data) {
        $("#dataSent").val(unescape(f_data));
        let f_contentType = 'application/json; charset=UTF-8';
        $.ajax({
            url: f_url,
            type: f_method,
            contentType: f_contentType,
            dataType: 'json',
            data: f_data,
            success: function (data) {
                let jsonResult = JSON.stringify(data);
                $("#results").val(unescape(jsonResult));
            }
        });
    }

    $("#alarmForm").on('submit',function(event) {
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
        console.log(data);
        ajaxCallRequest(method, url, data);
    });
});