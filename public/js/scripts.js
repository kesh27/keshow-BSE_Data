$(document).ready(function() {
    $.ajax({
        type: "GET",
        url: "/generator",
        success: function(response) {
            response = JSON.parse(response)
            console.log(response)
        }
    }) 
});
