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


// NEED TO ADD AN EVENT LISTENER FOR THE HIDE BUTTON!!!!
// REMOVE THE DIV FROM THE TIMELINE
// CHANGE THE ACTIVITY OF THE ARTICLE TO FALSE
// ADD LOGIC TO THE TIMELINE ROUTE TO ONLY DISPLAY ARTICLES THAT ARE ACTIVE=TRUE

// The problem here is that if I change the activity of the article... then the article will not appear
// for any of the users. 