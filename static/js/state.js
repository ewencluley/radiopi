let socket = io();
socket.on('state_update', function(data) {
        loading()
        console.log('got state update', data)
        let state = JSON.parse(data)
        $("#alarmTime").val(state.alarm.time)
        $("#alarmDuration").val(state.alarm.durationMinutes)
        $("#alarmEnabled").prop('checked', state.alarm.enabled).change()
        for (let i = 0; i < 7; i++) {
            if (state.alarm.daysOfWeek.includes(i)) {
                $("#daysOfWeek :input[value=" + i + "]").attr('checked', true)
                $("#daysOfWeek :input[value=" + i + "]").parent().addClass('active')
            }
        }
        $('#stopAlarm').prop('disabled', !state.alarm.isSounding)
        $("#radio").prop('checked', state.radio.on).change();
        loading_complete()
        console.log("inflight loading:", inflight_loading_requests)
});