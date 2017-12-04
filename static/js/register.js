"use strict";

$('document').ready(function() {

    $('.registration').click(function (evt) {
        evt.preventDefault();
        $('.registration-form').removeClass("hidden");
        $('.signin-form').addClass("hidden");

    });

    $('.signin').click(function (evt) {
        evt.preventDefault();
        $('.registration-form').addClass("hidden");
        $('.signin-form').removeClass("hidden");

    });
});
