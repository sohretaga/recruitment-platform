const selectedLanguage = document.getElementById('selected-language');
const languages = document.querySelectorAll('.language');

languages.forEach((language) => {
    language.addEventListener('click', () => {
        let image = language.querySelector('img');
        let code = language.getAttribute('data-code');

        selectedLanguage.querySelector('img').src = image.src;
        selectedLanguage.setAttribute('data-code', code);

        setLanguage(code);
    });
});

const setLanguage = (code) => {

    fetch('/language/set-language', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        },
        body: JSON.stringify({
            language: code,
            url:  window.location.pathname,
        })
    })
    .then(response => {
        if (response.ok) {
            window.location.reload();
        };
    });
}