var featuredSwiper = new Swiper(".featured-swiper", {
    spaceBetween: 30,
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
    mousewheel: true,
    keyboard: true,
  });

  var companySwiper = new Swiper(".company-swiper", {
    slidesPerView: 3,
    spaceBetween: 30,
    freeMode: true,
    autoplay: {
      delay: 2500,
      disableOnInteraction: false,
    },
  });