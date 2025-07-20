function getCookie(name) {
    let cookieValue = null
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';')
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim()
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
                break
            }
        }
    }
    return cookieValue;
}

function make_click() {
    const csrftoken = getCookie('csrftoken')
    let response = fetch("/clicker/", {
       method: 'POST',
       headers: {
           "X-CSRFToken": csrftoken
       }
    })
    .then(response => response.json())
    .then(data => {
        num_of_click.innerText = "Кол-во: " + data.number_of_click
    })
}