var targetNode = document.querySelector('li.next a');
var nextBtn = document.querySelector('li.next');
var previousBtn = document.querySelector('li.previous a');

var config = { attributes: true, attributeFilter: ['class'] };

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
                    console.log('form submit');
                    
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