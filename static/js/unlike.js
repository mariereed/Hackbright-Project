"use strict";

$('document').ready(function() {
    function removeArticle(results) {
        if (results.confirm === true) {
            console.log('Imade it into removeA');
            console.log('div-' + String(results.id));
            let theDiv = $('div-' + String(results.id));
            theDiv.remove();
        }
    }

    function likeArticle(evt) {
        $.post('/unlike', {'articleId': this.id}, removeArticle);
    }

    $('.like').on('click', likeArticle);
});
