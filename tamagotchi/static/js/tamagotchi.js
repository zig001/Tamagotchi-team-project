function updateTime(){
    var timeNow = new Date()
    var hoursNow = timeNow.getHours()
    var minutesNow = timeNow.getMinutes()

    clock.innerText = `${hoursNow.toString().padStart(2,'0')}:${minutesNow.toString().padStart(2,'0')}`
}

updateTime()
setInterval(updateTime, 1000)

let weather

async function getWeather() {
    let response = await fetch('https://wttr.in/Moscow?format=j1')
    if (response.status === 200) {
        let weatherData = await response.json()
        return weatherData.current_condition[0].weatherDesc[0].value
    } else {
        throw new Error('Не удалось получить данные о погоде')
    }
}

function updateWeatherInfo() {
    if (weather.includes('Sunny')) {
        roomBackground.style.backgroundImage = `url('/static/img/rooms/${currentRoom}/bright.png')`
    } else if (weather.includes('Clear')) {
        roomBackground.style.backgroundImage = `url('/static/img/rooms/${currentRoom}/bright.png')`
    } else if (weather.includes('Partly-cloudy')) {
        roomBackground.style.backgroundImage = `url('/static/img/rooms/${currentRoom}/pasmurno.png')`
    } else if (weather.includes('Cloudy')) {
        roomBackground.style.backgroundImage = `url('/static/img/rooms/${currentRoom}/pasmurno.png')`
    } else if (weather.includes('Rain')) {
        roomBackground.style.backgroundImage = `url('/static/img/rooms/${currentRoom}/rainy.png')`
    } else if (weather.includes('Overcast')) {
        roomBackground.style.backgroundImage = `url('/static/img/rooms/${currentRoom}/pasmurno.png')`
    } else if (weather.includes('Snow')) {
        roomBackground.style.backgroundImage = `url('/static/img/rooms/${currentRoom}/snowy.png')`
    } else if (weather.includes('Heavy rain and snow shower')) {
        roomBackground.style.backgroundImage = `url('/static/img/rooms/${currentRoom}/rainy.png')`
    } else {
        roomBackground.style.backgroundImage = `url('/static/img/rooms/${currentRoom}/pasmurno.png')`
    }
}

async function updateWeather() {
    weather = await getWeather()
    updateWeatherInfo()
}

updateWeather()
setInterval(updateWeather, 600000)