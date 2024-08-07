const languageSelect = document.querySelector("select[name='language']");
const titleInputEN = document.querySelector("input[name='title_en']");
const titleInputTR = document.querySelector("input[name='title_tr']");
const contentInputEN = document.getElementById('content-en');
const contentInputTR = document.getElementById('content-tr');

languageSelect.addEventListener('change', (select) => {
    let language_code = select.target.value;

    if (language_code == 'en') {
        titleInputEN.style.display = 'inline';
        contentInputEN.style.display = 'inline';

        titleInputTR.style.display = 'none';
        contentInputTR.style.display = 'none';
    }
    else if (language_code == 'tr') {
        titleInputEN.style.display = 'none';
        contentInputEN.style.display = 'none';

        titleInputTR.style.display = 'inline';
        contentInputTR.style.display = 'inline';
    };
});