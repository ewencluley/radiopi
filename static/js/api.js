let inflight_saving_requests = 0
let inflight_loading_requests = 0

function saving() {
    if (inflight_saving_requests === 0) {
        $("#savingIcon").attr("class", "fas fa-circle-notch fa-spin")
    }
    inflight_saving_requests += 1
}
function saving_complete() {
    if (inflight_saving_requests > 0) {
        inflight_saving_requests -= 1
    }
    if (inflight_saving_requests <= 0) {
        $("#savingIcon").attr("class", "fas fa-check-circle")
    }
}
function loading() {
    inflight_loading_requests += 1
}
function loading_complete() {
    if (isLoading()) {
        inflight_loading_requests -= 1
    }
    if (inflight_loading_requests <= 0) {
        console.log("loading complete");
    }
}
function isLoading() {
    return inflight_loading_requests > 0
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