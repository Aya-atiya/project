const form = document.querySelector('form');
const input = document.querySelector('input[name="input"]');
const output = document.querySelector('#output');

form.addEventListener('submit', (event) => {
    event.preventDefault();
    output.innerHTML += '<p>You entered: ' + input.value + '</p>';
    input.value = '';
});
