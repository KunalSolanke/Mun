"use strict";

var countries,
    nav_toggle,
    main_div,
    sidebar,
    width,
    loadingWrapper = document.querySelector('.load'),
    afterLoad = document.querySelector('.after__load');
window.addEventListener('load', function () {
  SetMessages("initial");
  countries = document.querySelectorAll('.country');
  countries.forEach(function (country) {
    country.addEventListener('click', function () {
      inputField.value = country.querySelectorAll('div')[1].innerText;
      countries.forEach(function (c) {
        c.classList.remove('added');
      });
      country.classList.add("added");
      inputFieldDev.classList.add('clicked');
      inputField.classList.add('clicked');
      setTimeout(function () {
        inputFieldDev.classList.remove('clicked');
        inputField.classList.remove('clicked');
      }, 1200);
    });
  }); //nav_toggle

  nav_toggle = document.querySelector('.nav__toggle');
  main_div = document.querySelector('.main_div');
  sidebar = document.querySelector('.sidebar');
  nav_toggle.addEventListener('click', function (e) {
    width = sidebar.clientWidth;

    if (!nav_toggle.classList.contains('active')) {
      nav_toggle.classList.add('active');
      main_div.style.transform = "translateX(".concat(width, "px)");
    } else {
      nav_toggle.classList.remove('active');
      main_div.style.transform = "translateX(0px)";
    }
  });
  setTimeout(function () {
    afterLoad.classList.add('active');
    loadingWrapper.classList.add('inactive');
  }, 1000);
});