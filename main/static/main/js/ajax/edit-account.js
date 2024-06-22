const selects = document.querySelectorAll('select');

selects.forEach(select => {
    new Choices(`#${select.name}`)
});

const profileImg = document.getElementById('profile-img');
const previewImg = (input) => {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            document.getElementById('profile-img').src = e.target.result;
        };
        reader.readAsDataURL(input.files[0]);
    };
};