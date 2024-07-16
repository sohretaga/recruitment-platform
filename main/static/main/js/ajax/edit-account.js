const selects = document.querySelectorAll('select');
const galleryImages = document.getElementById('gallery-images');
const limitAlert = document.getElementById('limit-alert');

selects.forEach(select => {
    new Choices(`#${select.id}`)
});


// Collects the values ​​selected from the Language selection into an input and prepares it for recording.
const languages = document.getElementById('languages');
const languageValuesInput = document.getElementById('langauge-values');
if (languages) {
    languages.addEventListener('change', function() {
        let values = new Array();
        languages.querySelectorAll('option').forEach((option) => {
            values.push(option.value);
        });
        languageValuesInput.value = values;
    });
};
// End

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

const genHexString = () => {
    const hex = '456789ABCDEF';
    let output = '';
    for (let i = 0; i < 3; ++i) {
        output += hex.charAt(Math.floor(Math.random() * hex.length));
    }
    return output;
}

const previewGalleryImage = (event, id) => {
    const input = event.target;
    const reader = new FileReader();
    reader.onload = function(){
        const dataURL = reader.result;
        const imageUploadWrapper = document.getElementById(`image-upload-wrapper-${id}`);
        const uploadedImage = document.getElementById(`uploadedImage-${id}`);
        uploadedImage.src = dataURL;
        imageUploadWrapper.classList.add('has-image');
    };
    reader.readAsDataURL(input.files[0]);
};

const deleteImage = (button) => {
    const parentDiv = button.closest('.d-flex.justify-content-between');
    const image_id = parentDiv.id;
    parentDiv.remove();
    limitAlert.style.display = 'none';

    if (image_id) {
        $.ajax({
            url: '/ajax-delete-gallery-image',
            type: 'POST',
            data: {image_id: image_id},
        });
    };
};

const addImage = () => {
    const randomId = genHexString();
    const galleryLength = galleryImages.children.length;

    if (galleryLength < 5) {
        galleryImages.insertAdjacentHTML('beforeend', `
        <div class="d-flex justify-content-between mb-5">
            <input type="hidden" name="image-id" value="${randomId}">
            <div class="image-upload-wrapper" id="image-upload-wrapper-${randomId}" onclick="document.getElementById('imageUpload-${randomId}').click();">
                <img id="uploadedImage-${randomId}" src="" alt="Uploaded Image">
                <input name="image-${randomId}" type="file" id="imageUpload-${randomId}" accept="image/*" style="display: none;" onchange="previewGalleryImage(event, '${randomId}')">
            </div>
            <div class="ms-3 w-100">
                <div class="d-flex">
                    <input name="title" type="text" class="form-control mb-2" placeholder="Title">
                    <button class="btn btn-danger fs-17 mb-2 ms-3" onclick="deleteImage(this)"><i class="uil uil-trash-alt"></i></button>
                </div>
                <textarea name="description" class="form-control" rows="3" placeholder="Description"></textarea>
            </div>
        </div>`);
    } else {
        const a = document.createElement('a');
        a.href = '#pills-tab';
        a.click();
        a.remove();

        limitAlert.style.display = 'block';
    };
};