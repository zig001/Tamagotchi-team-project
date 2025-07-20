let currentRoom = 'living_room'
let sleept = actionButton.innerText === 'Проснуться' ? true : false

function execute_operation() {
    switch (currentRoom) {
        case ('living_room'): 
            let response = fetch(`/api/rest_activity`)
            .then(response => response.json())
            .then(data => {
                if (data['code'] === 1){
                    night.classList.add('visible')
                    actionButton.innerText = 'Проснуться'
                    sleept = true
                } else if (data['code'] === 2){
                    night.classList.remove('visible')
                    actionButton.innerText = 'Лечь спать'
                    sleept = false
                }
            })
            break
        case ('kitchen'):
            show_banner('market')
            break
        case ('bathroom'):
            break
        case ('playground'):
            break
    }
    
}

async function buy(item) {
    let response = await fetch(`/api/buy_food?food=${item}`)
    if (response.status === 200) {
        let data = await response.json()
        numberOfClick.innerText = data['number_of_click']
        tamagotchiHealth.style.width = data['tamagotchi_mood']['health'] + '%'
        tamagotchiHunger.style.width = data['tamagotchi_mood']['hunger'] + '%'
        tamagotchiRest.style.width = data['tamagotchi_mood']['rest'] + '%'
    }
}

function updateRoom(room) {
    show_banner('goto')
    updateLiving_room.style.display = 'block'
    updateKitchen.style.display = 'block'
    updateBathroom.style.display = 'block'
    updatePlayground.style.display = 'block'
    night.classList.remove('visible')
    switch (room) {
        case ('living_room'):
            currentRoom = 'living_room'
            updateWeatherInfo()

            updateLiving_room.style.display = 'none'
            infoText.innerHTML = 'В гостинной вы можете восполнить силы своего питомца, отправив его спать <br><br><span style="font-style: italic;">Сон востанавливает <b>бодрость</b>, но сильно увеличивает чувство <b>голода</b></span>'
            if (sleept) {
                night.classList.add('visible')
            }
            actionButton.innerText = sleept ? 'Проснуться' : 'Лечь спать'
            break
        case ('kitchen'):
            currentRoom = 'kitchen'
            updateWeatherInfo()

            updateKitchen.style.display = 'none'
            infoText.innerHTML = 'На кухне вы можете востановить голод своего питомца <br><br><span style="font-style: italic;">Зарабатывая очки в <a href="/clicker/">кликере</a> вы можете потратить их на еду в <a onclick="show_banner(`market`)">магазине</a> для тамагочи</span>'
            actionButton.innerText = 'Магазин'
            break
        case ('bathroom'):
            currentRoom = 'bathroom'
            updateWeatherInfo()

            updateBathroom.style.display = 'none'
            infoText.innerHTML = 'В ванной комнате вы можете умыть своего питомца <br><br><span style="font-style: italic;">Немного восстанавливает <b>здоровье</b>, но уменьшает <b>бодрость</b></span>'
            actionButton.innerText = 'Умыться'
            break
        case ('playground'):
            currentRoom = 'playground'
            updateWeatherInfo()

            updatePlayground.style.display = 'none'
            infoText.innerHTML = 'Во дворе вы можете поиграть со своим питомцем <br><br><span style="font-style: italic;">Востанавливает <b>здоровье</b>, но увеличивает чувство <b>голода</b> и уменьшает <b>бодрость</b></span>'
            actionButton.innerText = 'Поиграть'
            break
    }
}

function show_banner(name){
    switch(name){
        case 'goto':
            stats.classList.remove('visible')
            info.classList.remove('visible')
            market.classList.remove('visible')
            goto.classList.toggle('visible')
            break
        case 'stats':
            goto.classList.remove('visible')
            info.classList.remove('visible')
            market.classList.remove('visible')
            stats.classList.toggle('visible')
            break
        case 'info':
            goto.classList.remove('visible')
            stats.classList.remove('visible')
            market.classList.remove('visible')
            info.classList.toggle('visible')
            break
        case 'market':
            goto.classList.remove('visible')
            stats.classList.remove('visible')
            info.classList.remove('visible')
            market.classList.toggle('visible')
            break
    }
}

function updateStats() {
    let response = fetch(`/api/get_stats`)
    .then(response => response.json())
    .then(data => {
        tamagotchiHealth.style.width = data['health'] + '%'
        tamagotchiHunger.style.width = data['hunger'] + '%'
        tamagotchiRest.style.width = data['rest'] + '%'
    })
}

setInterval(updateStats, 60000)