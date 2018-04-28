$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#inputID").val(res.id);
        $("#inputUsername").val(res.username);
        $("#inputPassword").val(res.password);
        $("#inputEmail").val(res.email);
        $("#inputFirstname").val(res.firstname);
        $("#inputLastname").val(res.lastname);
        $("#inputPhone").val(res.phone);
        $("#inputAddress").val(res.address);
        if (res.active == true) {
            $("#inputActive").val("true");
        } else {
            $("#inputActive").val("false");
        }
        if (res.promo == true) {
            $("#inputPromo").val("true");
        } else {
            $("#inputPromo").val("false");
        }
    }

    // Clears all form fields
    function clear_form_data() {
        $("#pet_name").val("");
        $("#pet_category").val("");
        $("#pet_available").val("");

        $("#inputID").val("");
        $("#inputUsername").val("");
        $("#inputPassword").val("");
        $("#inputEmail").val("");
        $("#inputFirstname").val("");
        $("#inputLastname").val("");
        $("#inputPhone").val("");
        $("#inputAddress").val("");
        $("#inputActive").val("");
        $("#inputPromo").val("");
    }

    // ****************************************
    // Retrieve a Customers
    // ****************************************
    $("#retrieve-btn").click(function () {
        var customer_id = $("#inputID").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/customers/" + customer_id,
            contentType:"application/json",
            data: ''
        });

        ajax.done(function(res){
            update_form_data(res)
        });

        ajax.fail(function(res){
            clear_form_data()
        });
    });


    // ****************************************
    // Search for a Customer
    // ****************************************

    // $("#search-btn").click(function () {
    //
    //     var username = $("#customer_username").val();
    //     var password = $("#customer_password").val();
    //     var firstname = $("#customer_firstname").val();
    //     var secondname = $("#customer_secondname").val();
    //     var address = $("#customer_address").val();
    //     var phone = $("$customer_phone").val();
    //     var email = $("$customer_email").val();
    //     var status_val = $("#customer_status").val();
    //     var promo = $("#customer_promo").val();
    //
    //     var queryString = ""
    //
    //     if (username) {
    //         queryString += 'username=' + name
    //     }
    //     if (password) {
    //         if (queryString.length > 0) {
    //             queryString += '&password=' + password
    //         } else {
    //             queryString += 'password=' + password
    //         }
    //     }
    //     if (firstname) {
    //         if (queryString.length > 0) {
    //             queryString += '&firstname=' + firstname
    //         } else {
    //             queryString += 'firstname=' + firstname
    //         }
    //     }
    //     if (lastname) {
    //         if (queryString.length > 0) {
    //             queryString += '&lastname=' + lastname
    //         } else {
    //             queryString += 'lastname=' + lastname
    //         }
    //     }
    //     if (address) {
    //         if (queryString.length > 0) {
    //             queryString += '&address=' + address
    //         } else {
    //             queryString += 'address=' + address
    //         }
    //     }
    //     if (phone {
    //         if (queryString.length > 0) {
    //             queryString += '&phone=' + phone
    //         } else {
    //             queryString += 'phone=' + phone
    //         }
    //     }
    //     if (email) {
    //         if (queryString.length > 0) {
    //             queryString += '&email=' + email
    //         } else {
    //             queryString += 'email=' + email
    //         }
    //     }
    //     if (status_val) {
    //         if (queryString.length > 0) {
    //             queryString += '&status=' + status_val
    //         } else {
    //             queryString += 'status=' + status_val
    //         }
    //     }
    //
    //     if (promo) {
    //         if (queryString.length > 0) {
    //             queryString += '&promo=' + promo
    //         } else {
    //             queryString += 'promo=' + promo
    //         }
    //     }
    //
    //     var ajax = $.ajax({
    //         type: "GET",
    //         url: "/customers?" + queryString,
    //         contentType:"application/json",
    //         data: ''
    //     })
    //
    //     ajax.done(function(res){
    //         //alert(res.toSource())
    //         $("#search_results").empty();
    //         $("#search_results").append('<table class="table-striped">');
    //         var header = '<tr>'
    //         header += '<th style="width:10%">ID</th>'
    //         header += '<th style="width:10%">UserName</th>'
	  //   header += '<th style="width:10%">Password</th>'
	  //   header += '<th style="width:10%">FirstName</th>'
    //         header += '<th style="width:10%">LastName</th>'
    //         header += '<th style="width:10%">Address</th>'
    //         header += '<th style="width:10%">Phone</th>'
    //         header += '<th style="width:10%">Email</th>'
    //         header += '<th style="width:10%">Status</th>'
    //         header += '<th style="width:10%">Promo</th></tr>'
    //         $("#search_results").append(header);
    //         for(var i = 0; i < res.length; i++) {
    //             customer = res[i];
    //             var row = "<tr><td>"+customer.id+"</td><td>"+customer.username+"</td><td>"+customer.password+"</td><td>"+customer.firstname+"</td><td>"+customer.lastname+"</td><td>"+customer.address+"</td><td>"+customer.phone+"</td><td>"+customer.email+"<td></td>"+customer.status_val+"<td></td>"+customer.promo+"</td></tr>";
    //             $("#search_results").append(row);
    //         }
    //
    //         $("#search_results").append('</table>');
    //
    //         flash_message("Success")
    //     });
    //
    //     ajax.fail(function(res){
    //         flash_message(res.responseJSON.message)
    //     });
    //
    // });

})
