function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

$(document).ready(function() {
    $(".like-button").click(function(event) {
        event.preventDefault();

        let postId = $(this).data("post-id"); 
        let likeIcon = $("#heart-like-" + postId);
        let likeCount = $("#like-count-" + postId);

        $.ajax({
            type: "POST",
            url: window.location.href, 
            data: {
                "post-id": postId,
                "like-post-btn": "true",
                "csrfmiddlewaretoken": getCSRFToken()
            },
            headers: { "X-Requested-With": "XMLHttpRequest" },
            
            success: function(response) {
                if (response.liked) {
                    likeIcon.removeClass("fa-regular").addClass("fa-solid");
                } else {
                    likeIcon.removeClass("fa-solid").addClass("fa-regular");
                }
                likeCount.text(response.likes);
            },
            error: function(response) {
                console.error("Erro ao curtir postagem", response);
            }
        });
    });
});