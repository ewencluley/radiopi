$(document).ready(function() {
    $("#radio").on('submit', event => event.preventDefault());
    $("#radio").change(function() {
        if (isLoading()) {
            return;
        }
        saving();
        ajaxCallRequest("PATCH", "/api/v1/radio", JSON.stringify({"radioOn": $(this).prop('checked')}), saving_complete);
    });
    $("#volume").change(function() {
        if (isLoading()) {
            return;
        }
        saving();
        ajaxCallRequest("PATCH", "/api/v1/radio", JSON.stringify({"volume": $(this).val()}), saving_complete);
    });
});

function changeStation(url) {
    ajaxCallRequest("PATCH", "/api/v1/radio", JSON.stringify({"currentStation": url}), saving_complete);
    console.log("changed station to:", url)
}