$(document).ready(function() {

    $(".tweet-text").each(function() {
        var text = $(this);
        const tag_re = /#(\w+)/g; // Regex to match hashtags
        const mention_re = /@(\w+)/g; // Regex to match mentions

        // Get the text content
        var newText = text.text();

        // Replace hashtags with <a> tags
        newText = newText.replace(tag_re, '<a class="hashtags" href="/explore/$1">#$1</a>');

        // Replace mentions with <a> tags
        newText = newText.replace(mention_re, '<a class="mentions" href="/user/$1">@$1</a>');


        // Update the element's HTML with the new content
        text.html(newText);
    });

    $(".tweet-text").each(function() {
        var queryParams = new URLSearchParams(window.location.search);

        // Get a specific parameter
        var keyword = queryParams.get('q');
        
        var text = $(this);

        // Get the text content
        var newText = text.text();

        // Replace hashtags with <a> tags
        newText = newText.replace(keyword, '<span class="highlight">' + keyword + '</span>');

        // Update the element's HTML with the new content
        text.html(newText);
    });

    $(".tweet-image").click(function() {
        console.log("image was clicked")
    });

    $(".liked").each(function() {
        var button = $(this);
        var svgIcon = button.find('svg');
        svgIcon.attr('stroke', 'none');
        svgIcon.addClass('fill-current');
        button.addClass('text-red-500');
    });

    $(".retweeted").each(function() {
        var button = $(this);
        var svgIcon = button.find('svg');
        button.addClass('text-green-500');
    });

    $(".like-btn").click(function() {
        var postId = $(this).data("post-id");
        var button = $(this);
        var svgIcon = button.find('svg');
        var count = button.find('.count');

        $.ajax({
            url: "/tweet/" + postId + "/like/",
            type: "POST",
            headers: { "X-CSRFToken": csrf_token },
            success: function(response) {
                if (response.liked) {
                    count.text(Number(count.text()) + 1);
                    // svgIcon.attr('stroke', 'none');
                    svgIcon.addClass('fill-current');
                    button.addClass('liked');


                } else if (!response.liked) {
                    like_count = Number(count.text())
                    if (like_count > 0) {
                        count.text(like_count - 1)};
                    // svgIcon.attr('stroke', 'currentColor');
                    svgIcon.removeClass('fill-current');
                    // button.removeClass('text-red-500');
                    button.removeClass('liked');


                }
            }
        });
    });

    $(".retweet-btn").click(function() {
        var postId = $(this).data("post-id");
        var button = $(this);
        var svgIcon = button.find('svg');
        var count = button.find('.count');

        $.ajax({
            url: "/tweet/" + postId + "/retweet/",
            type: "POST",
            headers: { "X-CSRFToken": csrf_token },
            success: function(response) {
                console.log(response)
                if (response.retweeted) {
                    count.text(Number(count.text()) + 1);
                    button.addClass('retweeted');

                } else if (!response.retweeted){

                    retweet_count = Number(count.text())
                    if (retweet_count > 0) {
                        count.text(retweet_count - 1)};
                    button.removeClass('retweeted');

                    
                }
            }
        });
    });


});

function showPage(pageId, event) {
    // Hide all pages
    $('.page').addClass('hidden');

    // Show the selected page
    $('#' + pageId).removeClass('hidden');

    // Remove active styles from all buttons
    $('button').removeClass('text-blue-500 border-b-2 border-blue-500');

    // Add active styles to the clicked button
    $(event.target).addClass('text-blue-500 border-b-2 border-blue-500');
}