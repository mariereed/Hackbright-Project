"use strict";

function changeButton(results) {
    let confirmBoole = results;
    console.log('I made it into the changeButton function.');
    // may not be able to jsonify a boolean
    if (confirmBoole === 'True') {
        // change color of button with id = 'like'
        let theLikeButton = document.querySelector('.like');
        theLikeButton.style.color = 'red';
    }
}

function likeArticle(evt) {
    // Does this do what I think it does???
    console.log('I made it into the likeArticle function.');
    $.post('/like', {'articleId': $('.like').attr('id')}, changeButton);
}
$('document').ready(function() {
    $('.like').on('click', likeArticle);
})

console.log('I made it to the JS file');