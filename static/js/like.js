"use strict";

$('document').ready(function() {
    function changeButton(results) {
        console.log('I made it into the changeButton function.');
        // may not be able to jsonify a boolean
        if (results.confirm === true) {
            // How do I get this bound?
            console.log('i made it past the confirmation');
            console.log(results.id);
            console.log(String(results.id));
            console.log('#' + results.id);
            let theLikeButton = document.getElementById(results.id);
            theLikeButton.style.color = 'red';
        }
    }

    function likeArticle(evt) {
        // Does this do what I think it does???
        console.log('I made it into the likeArticle function.');
        console.log(this.id);
        $.post('/like', {'articleId': this.id}, changeButton);
    }

    $('.like').on('click', likeArticle);
});

console.log('I made it to the JS file');