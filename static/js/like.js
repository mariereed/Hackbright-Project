"use strict";

$('document').ready(function() {
    function changeButton(results) {
        if (results.confirm === true) {
            let theLikeButton = document.getElementById(results.id);
            theLikeButton.style.color = 'red';
            theLikeButton.className = 'favorited';
        }
    }

    function likeArticle(evt) {
        $.post('/like', {'articleId': this.id}, changeButton);
    }

    $('.like').on('click', likeArticle);
});
