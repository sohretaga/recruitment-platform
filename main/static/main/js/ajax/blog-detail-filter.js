const redirectUrl = () => {
    const checkboxes = document.querySelectorAll('#blog-categories input[type="checkbox"]');
    const selectedCheckboxes = Array.from(checkboxes).filter(checkbox => checkbox.checked);
    const selectedValues = selectedCheckboxes.map(checkbox => checkbox.value);

    window.location.assign(`/blog/?categories=${selectedValues.join(',')}#blog-list`)
};

const addCheckboxListener = (selector, callback) => {
    const checkboxes = document.querySelectorAll(selector);
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', callback);
    });
};

addCheckboxListener('#blog-categories input[type="checkbox"]', redirectUrl); // Categories Listener