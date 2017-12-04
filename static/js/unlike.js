"use strict";

$('document').ready(function() {
    function unlikeArticle(results) {
        if (results.confirm === true){
            let theDiv = $('#div-' + String(results.id));
            theDiv.remove();
        }
    }

    function likeArticle(evt) {
        $.post('/unlike', {'articleId': this.id}, unlikeArticle);
    }

    $('.like').on('click', likeArticle);
});