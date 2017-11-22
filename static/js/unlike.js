"use strict";

$('document').ready(function() {
    function removeArticle(results) {
        if (results.confirm === true) {
            let theDiv = $('#div-' + String(results.id));
            theDiv.remove();
        }
    }

    function likeArticle(evt) {
        $.post('/unlike', {'articleId': this.id}, removeArticle);
    }

    $('.like').on('click', likeArticle);
});
