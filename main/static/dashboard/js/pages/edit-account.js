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

(function($) {
    "use strict";
    
    // Constructor function
    function AdvancedForm() {}

    // Initialize function
    AdvancedForm.prototype.init = function() {
        // Select2 initialization
        $(".select2").select2();
        $(".select2-limiting").select2({ maximumSelectionLength: 2 });
        $(".select2-search-disable").select2({ minimumResultsForSearch: Infinity });
    };

    // Initialize AdvancedForm
    $.AdvancedForm = new AdvancedForm();
    $.AdvancedForm.Constructor = AdvancedForm;

})(window.jQuery);

// Initialize the script
(function() {
    "use strict";
    window.jQuery.AdvancedForm.init();
})();
