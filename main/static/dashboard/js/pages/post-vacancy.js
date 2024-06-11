var targetNode = document.querySelector('li.next a');
var nextBtn = document.querySelector('li.next');
var previousBtn = document.querySelector('li.previous a');

var config = { attributes: true, attributeFilter: ['class'] };


// Select2 Config
(function(i) {
    "use strict";

    function a() {}

    a.prototype.init = function() {
        i(".select2").select2();
        
        // Set seleceted values
        var selectedValues = i("#keywordsInput").val().replace(/'/g, '"');
        i("#keywordsSelect").val(JSON.parse(selectedValues)).trigger('change');
        i("#keywordsInput").val(JSON.stringify(selectedValues));

        // Update hidden input on change
        i("#keywordsSelect").on('change', function() {
            var selectedValues = i(this).val();
            i("#keywordsInput").val(JSON.stringify(selectedValues));
            console.log(selectedValues)
        });
    };

    i.AdvancedForm = new a;
    i.AdvancedForm.Constructor = a;
})(window.jQuery);

(function() {
    "use strict";
    window.jQuery.AdvancedForm.init();
})();


var callback = function(mutationsList, observer) {
    for(var mutation of mutationsList) {
        if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
            var hasDisabledClass = targetNode.parentNode.classList.contains('disabled');
            if (hasDisabledClass) {
                targetNode.innerText = 'Post';
                nextBtn.classList.remove('disabled')
                targetNode.addEventListener('click', function(event) {
                    event.preventDefault();
                    document.getElementById('post-vacancy').submit();                    
                });
            }
        }
    }
};

var observer = new MutationObserver(callback);
observer.observe(targetNode.parentNode, config);

previousBtn.addEventListener('click', function(event) {
    targetNode.innerText = 'Next';
});