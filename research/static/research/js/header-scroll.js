(function() {
    var header = document.querySelector('.header-section');
    var lastScroll = 0;
    var scrollThreshold = 50;
    if (header) {
        window.addEventListener('scroll', function() {
            var currentScroll = window.pageYOffset;
            if (currentScroll > lastScroll && currentScroll > scrollThreshold) {
                header.classList.add('header-hidden');
            } else if (currentScroll < lastScroll) {
                header.classList.remove('header-hidden');
            }
            lastScroll = currentScroll <= 0 ? 0 : currentScroll;
        });
    }
})();
