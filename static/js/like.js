"use strict";

$('document').ready(function() {
    function changeButton(results) {
        if (results.confirm === true) {
            // let theLikeButton = document.getElementById(results.id);
            let theLikeButton = $('#' + String(results.id));
            // theLikeButton.style.color = 'red';
            theLikeButton.attr('style', "color:red");
        }
    }

    function likeArticle(evt) {
        $.post('/like', {'articleId': this.id}, changeButton);
    }

    $('.like').on('click', likeArticle);
});
