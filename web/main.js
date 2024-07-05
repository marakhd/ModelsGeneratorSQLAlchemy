let urlInput;
let btnSubmit;
let btnCopy;
let outputText;
let errorBox;

//let regex = /^(mysql|postgresql|sqlite):\/\/(?:[^\s@]+:[^\s@]+)@[^\s@]+(?::\d+)?\/[^\s?]+(?:\?[^#\s]+)?$/;
let regex = /^(mysql:\/\/[^\s@]+:[^\s@]+@[^\s@]+(?::\d+)?\/[^\s?]+(?:\?[^#\s]+)?|postgresql:\/\/[^\s@]+:[^\s@]+@[^\s@]+(?::\d+)?\/[^\s?]+(?:\?[^#\s]+)?|sqlite:\/\/\/[^\s?]+(?:\?[^#\s]+)?)$/;


async function display_data() {
    let element = "Ожидайте..."
    outputText.value = element;
    element = await eel.get_models(urlInput.value)();
    outputText.value = element;
}

function copy(id) {
    let el = document.querySelector(id);
    el.select();
    document.execCommand('copy');
}

document.addEventListener('DOMContentLoaded', () => {
    urlInput = document.querySelector('#url_input');
    btnSubmit = document.querySelector('#btn_submit');
    outputText = document.querySelector('#output');
    error = document.querySelector('#error')
    btnCopy = document.querySelector('#btn_copy')

    urlInput.value = localStorage.getItem('urlDb');

    btnSubmit.addEventListener('click', () => {
        if (urlInput.value) {
            regex.test(urlInput.value) ? display_data() : error.innerHTML = `
                Формат: driver://user:pass@url:port/dbname`
        } else if (!urlInput.value) {
            error.innerHTML = `
                Поле не должно быть пустым
            `
        }
    })
    btnCopy.addEventListener('click', () => {
        copy('#output')
    })
    urlInput.addEventListener('change', () => {
      localStorage.setItem('urlDb', urlInput.value);
    })
})