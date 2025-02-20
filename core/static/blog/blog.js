// Like Button Interaction
document.querySelectorAll('.like-btn').forEach(button => {
button.addEventListener('click', () => {
    button.classList.toggle('liked');
});
});

// Retweet Button Interaction
document.querySelectorAll('.retweet-btn').forEach(button => {
button.addEventListener('click', () => {
    button.classList.toggle('retweeted');
});
});
