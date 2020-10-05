$(document).ready(function() {
    $("#radio").on('submit', event => event.preventDefault());
    $("#radio").change(function() {
        if (isLoading()) {
            return;
        }
        saving();
        ajaxCallRequest("POST", "/api/v1/radio", JSON.stringify({"radioOn": $(this).prop('checked')}), saving_complete);
    });
});