$(document).ready(function() {

    $("#dropdown_button").click(function() {
        $("#my_dropdown").fadeIn(400);
    });
  
    $(window).on("click", function() {
        if (!$(event.target).is('#dropdown_button')) {
            $("#my_dropdown").fadeOut(400);
        }
    });

    $("#dropdown_button2").click(function() {
        $("#my_dropdown2").fadeIn(400);
    });
  
    $(window).on("click", function() {
        if (!$(event.target).is('#dropdown_button2')) {
            $("#my_dropdown2").fadeOut(400);
        }
    });

});