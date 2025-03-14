$(document).ready(function() {

    $(document).ready(function() {
        // Replace hashtags and mentions
        $(".tweet-text").each(function() {
            var text = $(this);
            const tag_re = /#(\w+)/g; // Regex to match hashtags
            const mention_re = /@(\w+)/g; // Regex to match mentions
    
            var newText = text.text();
    
            // Replace hashtags with <a> tags
            newText = newText.replace(tag_re, '<a class="hashtags" href="/explore/$1">#$1</a>');
    
            // Replace mentions with <a> tags
            newText = newText.replace(mention_re, '<a class="mentions" href="/user/$1">@$1</a>');
    
            // Update the element's HTML with the new content
            text.html(newText);
        });
    
        // Highlight keyword from URL
        var queryParams = new URLSearchParams(window.location.search);
        var keyword = queryParams.get('q'); // Get the keyword from the URL
    
        if (keyword) {
            // Escape special regex characters in the keyword
            const escapedKeyword = keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    
            // Create a regex with the 'gi' flags (global and case-insensitive)
            const keywordRegex = new RegExp(escapedKeyword, 'gi');
    
            $(".tweet-text").each(function() {
                var text = $(this);
                var newText = text.html(); // Use .html() to preserve existing links
    
                // Replace the keyword with a highlighted span
                newText = newText.replace(keywordRegex, '<span class="highlight">$&</span>');
    
                // Update the element's HTML with the new content
                text.html(newText);
            });
        }
    });

    $(document).ready(function() {
        // When a tweet image is clicked
        $(".tweet-image").click(function() {
            console.log("Image was clicked");
    
            // Get the source of the clicked image
            var imageSrc = $(this).attr("src");
    
            // Set the source of the enlarged image
            $("#enlarged-image").attr("src", imageSrc);
    
            // Show the overlay and image viewer
            $("#image-viewer-overlay").fadeIn();
        });
    
        // When the close button is clicked
        $("#close-image-viewer").click(function() {
            // Hide the overlay and image viewer
            $("#image-viewer-overlay").fadeOut();
        });
    
        // When the overlay is clicked (outside the image)
        $("#image-viewer-overlay").click(function(event) {
            if (event.target === this) {
                // Hide the overlay and image viewer
                $("#image-viewer-overlay").fadeOut();
            }
        });
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
            success: function(response, status) {
                console.log(status);
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
            },
            error: function(xhr, status, error) {
                // Handle any errors here, including redirects on error
                if (xhr.status == 302) {
                    // If the server responds with a redirect status code
                    var redirectUrl = xhr.getResponseHeader('Location');
                    window.location.href = redirectUrl;
                } else {
                    // Handle other errors
                    console.error("Error:", error);
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