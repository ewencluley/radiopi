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
                let dayOfWeekCheckbox = $("#daysOfWeek :input[value=" + i + "]");
                dayOfWeekCheckbox.attr('checked', true)
                dayOfWeekCheckbox.parent().addClass('active')
            }
        }
        $('#stopAlarm').prop('disabled', !state.alarm.isSounding)
        $("#radio").prop('checked', state.radio.on).change();

        let alarmTypeControl = $("#alarmType :input[value=" + state.alarm.type + "]");
        alarmTypeControl.attr("checked", true)
        alarmTypeControl.parent().addClass('active')
        $('#stationList').empty()
        state.radio.stations.forEach(station => {
            let stationElement = $(`<label class="btn btn-primary"><input type="radio" autocomplete="off">${station.name}</label>`).appendTo("#stationList")
            $(stationElement).children(":input").change(() => changeStation(station.url))
            if (state.radio.currentStation === station.url) {
                stationElement.addClass("active")
                stationElement.children("input").attr("checked", true)
            }
        })

        synchronize(new Date(Date.parse(state.time)))
        loading_complete()
        console.log("inflight loading:", inflight_loading_requests)
});

setInterval(function () {socket.emit("synchronize", null) }, 10000)