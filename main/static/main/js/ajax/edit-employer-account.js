const selects = document.querySelectorAll('select');
const galleryImages = document.getElementById('gallery-images');
const limitAlert = document.getElementById('limit-alert');
const menus = document.querySelectorAll('.edit-menu');
var tempImageId = 1;

selects.forEach(select => {
    if (select.id == 'organization_ownership'
        || select.id == 'sector'
        || select.id == 'number_of_employees'
        || select.id == 'organization_type' ) {
        new Choices(`#${select.id}`, {
            searchEnabled: false,
            shouldSort: false,
            shouldSortItems: false, 
            fuseOptions: {
                includeScore: true,
                threshold: 0.2,
                location: 0,
                useExtendedSearch: true,
            }
        });
    }else {
        new Choices(`#${select.id}`, {
            searchResultLimit: 500,
            resetScrollPosition: false,
            shouldSort: false,
            shouldSortItems: false, 
            fuseOptions: {
                includeScore: true,
                threshold: 0.2,
                location: 0,
                useExtendedSearch: true,
            }
        });
    };
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

const getGalleryPlaceholders = () => {
    const firstDiv = galleryImages.querySelector('div');
    const title = firstDiv.querySelector("input[name='title']").placeholder;
    const description = firstDiv.querySelector("textarea[name='description']").placeholder;

    return {
        title: title,
        description: description
    }
    
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
    const directDivs = Array.from(galleryImages.children).filter(el => el.tagName.toLowerCase() === 'div');

    if (directDivs.length > 1) {
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
};

const addImage = () => {
    const galleryLength = galleryImages.children.length;
    const placeholder = getGalleryPlaceholders();

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
                    <input name="title" type="text" class="form-control mb-2" placeholder="${placeholder.title}">
                    <button class="btn btn-danger fs-17 mb-2 ms-3" onclick="deleteImage(this)"><i class="uil uil-trash-alt"></i></button>
                </div>
                <textarea name="description" class="form-control" rows="3" placeholder="${placeholder.description}"></textarea>
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

const toggleMenu = (menuId) => {
    var menu = document.getElementById(menuId);
    var isMenuVisible = menu.style.display === 'block';
    closeAllMenus();
    if (!isMenuVisible) {
        menu.style.display = 'block';
    }
};

const closeAllMenus = () => {
    menus.forEach(function(menu) {
        menu.style.display = 'none';
    });
};

const removeImage = (imageId) => {
    var img = document.getElementById(imageId);

    $.ajax({
        url: '/ajax/delete-profile-image',
        type: 'POST',
        data: {image_id: imageId},
        success: function () {
            if (imageId == 'profile-img') {
                img.src = '/static/main/images/featured-job/default-company-img.jpeg';
            }else {
                img.src = '/static/main/images/featured-job/default-job-bg.jpg';
            };
        }
    });
};

document.addEventListener('click', function(event) {
    var isClickInsideMenu = event.target.closest('.profile-photo-edit') || event.target.closest('.edit-menu');
    if (!isClickInsideMenu) {
        closeAllMenus();
    }
});

// Tab settings
const url = new URL(window.location);
const tabButtons = document.querySelectorAll('[data-bs-toggle="pill"]');
const nextUrl = document.querySelectorAll('input[name="next"]');

tabButtons.forEach(button => {
    button.addEventListener('shown.bs.tab', (event) => {
        const targetTabId = event.target.getAttribute('data-bs-target').replace('#', '');
        updateUrlParameter('tab', targetTabId);
        updateNextInputs();
    });
});

const urlParams = new URLSearchParams(window.location.search);
const tabParam = urlParams.get('tab');
if (tabParam) {
    const targetTab = document.querySelector(`[data-bs-target="#${tabParam}"]`);
    if (targetTab) {
        const bootstrapTab = new bootstrap.Tab(targetTab);
        bootstrapTab.show();
    }
};

const updateUrlParameter = (param, value) => {
    if (value) {
        url.searchParams.set(param, value);
    } else {
        url.searchParams.delete(param);
    }
    window.history.replaceState({}, '', url);
};

const updateNextInputs = () => {
    nextUrl.forEach(input => {
        input.value = url.href;
    });
};


// WhatsApp Input
document.getElementById('whatsapp_number').addEventListener('input', function (e) {
    const allowedChars = /^[0-9+]*$/;

    if (!allowedChars.test(this.value)) {
        this.value = this.value.replace(/[^0-9+]/g, '');
    }
});