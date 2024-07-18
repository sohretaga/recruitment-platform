const selects = document.querySelectorAll('select');
const galleryImages = document.getElementById('gallery-images');
const limitAlert = document.getElementById('limit-alert');
var tempImageId = 1;

selects.forEach(select => {
    new Choices(`#${select.id}`)
});

const previewImg = (input) => {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            if (input.name == 'profile_photo') {
                document.getElementById('profile-img').src = e.target.result;
            }
            else if(input.name == 'background_image') {
                document.getElementById('background-img').src = e.target.result;
            };
        };
        reader.readAsDataURL(input.files[0]);
    };
};

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
    const galleryLength = galleryImages.children.length;

    if (galleryLength < 5) {
        galleryImages.insertAdjacentHTML('beforeend', `
        <div class="d-flex justify-content-between mb-5">
            <input type="hidden" name="image-id" value="t${tempImageId}">
            <div class="image-upload-wrapper" id="image-upload-wrapper-t${tempImageId}" onclick="document.getElementById('imageUpload-t${tempImageId}').click();">
                <img id="uploadedImage-t${tempImageId}" src="" alt="Uploaded Image">
                <input name="image-t${tempImageId}" type="file" id="imageUpload-t${tempImageId}" accept="image/*" style="display: none;" onchange="previewGalleryImage(event, 't${tempImageId}')">
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

    tempImageId += 1;
};