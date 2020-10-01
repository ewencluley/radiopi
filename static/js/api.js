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