$(document).ready(function() {
    $("#radio").change(function() {
        saving()
        ajaxCallRequest("POST", "/api/v1/radio", JSON.stringify({"radioOn": $(this).prop('checked')}), saving_complete)
    });

    ajaxCallRequest("GET", "/api/v1/radio", null, function (data) {
                $("#radio").prop('checked', data.radioOn).change()
            })
});