$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // ****************************************
    // Search for a Pet
    // ****************************************

    $("#search-btn").click(function () {

        var name = $("#pet_name").val();
        var category = $("#pet_category").val();
        var available = $("#pet_available").val() == "true";

        var queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        if (category) {
            if (queryString.length > 0) {
                queryString += '&category=' + category
            } else {
                queryString += 'category=' + category
            }
        }
        if (available) {
            if (queryString.length > 0) {
                queryString += '&available=' + available
            } else {
                queryString += 'available=' + available
            }
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/pets?" + queryString,
            contentType:"application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped">');
            var header = '<tr>'
            header += '<th style="width:10%">ID</th>'
            header += '<th style="width:40%">Name</th>'
            header += '<th style="width:40%">Category</th>'
            header += '<th style="width:10%">Available</th></tr>'
            $("#search_results").append(header);
            for(var i = 0; i < res.length; i++) {
                pet = res[i];
                var row = "<tr><td>"+pet.id+"</td><td>"+pet.name+"</td><td>"+pet.category+"</td><td>"+pet.available+"</td></tr>";
                $("#search_results").append(row);
            }

            $("#search_results").append('</table>');

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
