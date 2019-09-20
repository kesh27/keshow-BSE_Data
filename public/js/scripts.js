$(document).ready(function() {
    $("#generate-string").click(function(e) {
        $.ajax({
            type: "GET",
            url: "/generator"
        })
        e.preventDefault();
    });
});
