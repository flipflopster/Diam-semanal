$(document).ready(function() {

    $("#logged").on("dblclick", (function() {
        $(this).fadeOut(400);
    }));
    $("#name").click(function() {
        $("#logged").fadeIn(400);
    });


    $("#lstButton").click(function() {
        if( $("#lst").text().equals("Mostrar Lista de Quetsão")) {
            $("#lst").text("Esconder Lista de Questrão");
            $("#lst").show();
        } else {
            $("#lst").text("Mostrar Lista de Quetsão");
            $("#lst").hide();
        }
    });
    //    <script src="{% static 'script.js' %}"></script>
});
