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
        svgIcon.attr('stroke', 'currentColor');
        svgIcon.addClass('fill-current');
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
                    svgIcon.attr('stroke', 'none');
                    svgIcon.addClass('fill-current');
                    button.addClass('text-red-500');
                    button.addClass('liked');


                } else if (!response.liked) {
                    like_count = Number(count.text())
                    if (like_count > 0) {
                        count.text(like_count - 1)};
                    svgIcon.attr('stroke', 'currentColor');
                    svgIcon.removeClass('fill-current');
                    button.removeClass('text-red-500');

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
                if (response.retweeted) {

                    count.text(Number(count.text()) + 1);
                    svgIcon.attr('stroke', 'currentColor');
                    svgIcon.addClass('fill-current');
                    button.addClass('text-green-500');

                } else if (!response.retweeted){

                    count.text(Number(count.text()) - 1);
                    svgIcon.attr('stroke', 'currentColor');
                    svgIcon.removeClass('fill-current');
                    button.removeClass('text-red-500');
                    
                }
            }
        });
    });


});