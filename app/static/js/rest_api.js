$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#customer_username").val(res.customer_username);
        $("#customer_password").val(res.customer_password);
        $("#customer_firstname").val(res.customer_firstname);
        $("#customer_secondname").val(res.customer_secondname);
        $("#customer_address").val(res.customer_address);
        $("#customer_phone").val(res.customer_phone);
        $("#customer_email").val(res.customer_email);
        if (res.active == true) {
            $("#customer_active").val("true");
        } else {
            $("#customer_active").val("false");
        }
        if (res.promo == true) {
            $("#customer_promo").val("true");
        } else {
            $("#customer_promo").val("false");
        }
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#customer_name").val("");
        $("#customer_password").val("");
        $("#customer_firstname").val("");
        $("#customer_secondname").val("");
        $("#customer_address").val("");
        $("#customer_phone").val("");
        $("#customer_email").val("");
        $("#customer_active").val("");
        $("#customer_promo").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }


    // ****************************************
    // Search for a Customer
    // ****************************************

    // ****************************************
    // Retrieve a Pet
    // ****************************************

    $("#retrieve-btn").click(function () {

        alert("Entered")
        flash_message("Entered")
        var customer_id = $("#customer_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/customers/" + customer_id,
            contentType:"application/json",
            data: ''
        })

        ajax.done(function(res){
            alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });


    // ****************************************
    // Search for a Customer
    // ****************************************

    $("#search-btn").click(function () {
/*
        var username = $("#customer_username").val();
        var password = $("#customer_password").val();
        var firstname = $("#customer_firstname").val();
        var secondname = $("#customer_secondname").val();
        var address = $("#customer_address").val();
        var phone = $("$customer_phone").val();
        var email = $("$customer_email").val();
//        var active = $("#customer_active").val() == "true";
//        var promo = $("#customer_promo").val() == "true";

        var queryString = ""

        if (username) {
            queryString += 'username=' + username
        }
        if (password) {
            if (queryString.length > 0) {
                queryString += '&password=' + password
            } else {
                queryString += 'password=' + password
            }
        }
        if (firstname) {
            if (queryString.length > 0) {
                queryString += '&firstname=' + firstname
            } else {
                queryString += 'firstname=' + firstname
            }
        }
        if (lastname) {
            if (queryString.length > 0) {
                queryString += '&lastname=' + lastname
            } else {
                queryString += 'lastname=' + lastname
            }
        }
        if (address) {
            if (queryString.length > 0) {
                queryString += '&address=' + address
            } else {
                queryString += 'address=' + address
            }
        }
        if (phone) {
            if (queryString.length > 0) {
                queryString += '&phone=' + phone
            } else {
                queryString += 'phone=' + phone
            }
        }
        if (email) {
            if (queryString.length > 0) {
                queryString += '&email=' + email
            } else {
                queryString += 'email=' + email
            }
        }

        if (active) {
            if (queryString.length > 0) {
                queryString += '&active=' + active
            } else {
                queryString += 'active=' + active
            }
        }

        if (promo) {
            if (queryString.length > 0) {
                queryString += '&promo=' + promo
            } else {
                queryString += 'promo=' + promo
            }
        }
*/
        var ajax = $.ajax({
            type: "GET",
            //url: "/customers?" + queryString,
            url: "/customers",
            contentType:"application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped">');
            var header = '<tr>'
            header += '<th style="width:10%">ID</th>'
            header += '<th style="width:10%">UserName</th>'
	    header += '<th style="width:10%">Password</th>'
	    header += '<th style="width:10%">FirstName</th>'
            header += '<th style="width:10%">LastName</th>'
            header += '<th style="width:10%">Address</th>'
            header += '<th style="width:10%">Phone</th>'
            header += '<th style="width:10%">Email</th>'
            header += '<th style="width:10%">Active</th>'
            header += '<th style="width:10%">Promo</th></tr>'
            $("#search_results").append(header);
            for(var i = 0; i < res.length; i++) {
                customer = res[i];
                var row = "<tr><td>"+customer.id+"</td><td>"+customer.username+"</td><td>"+customer.password+"</td><td>"+customer.firstname+"</td><td>"+customer.lastname+"</td><td>"+customer.address+"</td><td>"+customer.phone+"</td><td>"+customer.email+"</td><td>"+customer.active+"</td><td>"+customer.promo+"</td></tr>";
//                 var row = "<tr><td>"+customer.id+"</td><td>"+customer.username+"</td><td>"+customer.firstname+"</td><td>"+customer.lastname+"</td></tr>";
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
