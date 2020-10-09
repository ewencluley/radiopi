var time = new Date()

function tick() {
    time.setSeconds(time.getSeconds() + 1)
    $('#time').html(time.format("HH:MM:ss"))
}

function synchronize(date) {
    time = date
}

setInterval(tick, 1000)