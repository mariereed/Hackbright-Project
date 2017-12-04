"use strict";

$('document').ready(function() {
    function changeButton(results) {
        if (results.confirm === true) {
            let theLikeButton = $('#' + String(results.id));
            theLikeButton.attr('style', "color:red");
            theLikeButton.removeClass('like');
            theLikeButton.addClass('unlike');
        }
    }
    

    function likeArticle(evt) {
        $.post('/like', {'articleId': this.id}, changeButton);
    }

    function hideArticle(results) {
        if (results.confirm === true) {
            let theDiv = $('#div-' + String(results.id));
            theDiv.addClass('hide');
        }
    }

    function deactiveateArticle(evt) {
        $.post('/hide', {'articleId': this.id}, hideArticle);
    }

    $('.like').on('click', likeArticle);
    $('.deactivate').on('click', deactiveateArticle);
});
