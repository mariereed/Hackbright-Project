"use strict";

$('document').ready(function() {
    function changeButton(results) {
        if (results.confirm === true) {
            let theLikeButton = $('#' + String(results.id));
            theLikeButton.attr('style', "color:red");
        }
    }

    function likeArticle(evt) {
        $.post('/like', {'articleId': this.id}, changeButton);
    }

    $('.like').on('click', likeArticle);
});


// NEED TO ADD AN EVENT LISTENER FOR THE HIDE BUTTON!!!!
// REMOVE THE DIV FROM THE TIMELINE
// CHANGE THE ACTIVITY OF THE ARTICLE TO FALSE
// ADD LOGIC TO THE TIMELINE ROUTE TO ONLY DISPLAY ARTICLES THAT ARE ACTIVE=TRUE